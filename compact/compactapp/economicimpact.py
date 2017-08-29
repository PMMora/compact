from .matrixtools import blank_matrix, \
    identity_matrix, \
    short_to_long, \
    long_to_short, \
    short_matrices_compatible, \
    list_to_sublists, \
    list_of_sublists_to_list_of_sums, \
    add_short, \
    subtract_short, \
    multiply_short, \
    divide_short,\
    transpose

from numpy.linalg import inv, det
import numpy

import os
import sqlite3

from .matches import naicsmatch, fipsmatch
from .UStable import raw_direct_requirements, industry_totals

# Query function copied from queries.py until directory is fixed
def select_column_yield(conn, column_name, fips, own, naics, year):
    '''return column from yield for a given area, industry, and year
        :param: fips_id is the 2 digit fips id
        :param: naics_id is the 3 or 6 digit naics id
        :param: year... well you know the year
    '''
    sql = '''SELECT {} FROM yield
                WHERE fips_id = '{}'
                    AND own_code = '{}'
                    AND naics_id = '{}'
                    AND year = '{}' '''.format(column_name,fips,own,naics,year)
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    return row


# This matches any given NAICS to its IO sector.
# If a user enters an invalid NAICS, raise a custom ValueError
def match_naics_to_IO(NAICS=111):
    match = naicsmatch
    IO = 0
    def loop(NAICS):
        try:
            IO = [pair['IO'] for pair in match if int(pair['NAICS']) == NAICS][0]
            return IO
        except:
            NAICS = str(NAICS)
            try:
                NAICS = int(NAICS[:len(NAICS) - 1])
                return loop(NAICS)
            except:
                raise ValueError('Invalid NAICS entered')
    return loop(NAICS)


#This matches a state to a fips:
def fips_match(state):
    for match in fipsmatch:
        if match['state'] == state:
            result = match['fips']
        else:
            pass
    return result


# Return a list of values 0 to 1 for each IO sector (1 through 66)
def determine_LQs(geo='Alabama', year=2015, lq_type='wages'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(os.path.dirname(base_dir), 'db.sqlite3')
    conn = sqlite3.connect(database)

    # Get the fips for our state for the query
    fips = fips_match(geo)

    # Create empty lists to add emp and wages to
    local = [{'IO': i+1, 'employees': 0, 'wages': 0} for i in range(0, 66)]
    us = [{'IO': i+1, 'employees': 0, 'wages': 0} for i in range(0, 66)]

    # Create empty lists to store erroneous NAICS if we need them
    localerrorlist = []
    userrorlist = []

    # Loop through every NAICS for every IO and add that emp and wage to the IO for the geo
    for io in local:
        for dic in naicsmatch:
            naics = dic['NAICS']
            if dic['IO'] == io['IO']:
                try:
                    io['employees'] += select_column_yield(conn, 'employees', fips, 5, naics, year)[0]
                    io['wages'] += select_column_yield(conn, 'wages', fips, 5, naics, year)[0]
                except:
                    localerrorlist.append(naics)

    # Loop through every NAICS for every IO and add that emp and wage to the IO for the US
    for io in us:
        for dic in naicsmatch:
            naics = dic['NAICS']
            if dic['IO'] == io['IO']:
                try:
                    io['employees'] += select_column_yield(conn, 'employees', 'US', 5, naics, year)[0]
                    io['wages'] += select_column_yield(conn, 'wages', 'US', 5, naics, year)[0]
                except:
                    userrorlist.append(naics)

    # Create 0 value variables for local and US emp and wages
    localtotalemp = 0
    localtotalwages = 0
    ustotalemp = 0
    ustotalwages = 0

    # Set those variables to equal the total emp and total wages for US and the local geo
    for dict in local:
        localtotalemp += dict['employees']
        localtotalwages += dict['wages']
    for dict in us:
        ustotalemp += dict['employees']
        ustotalwages += dict['wages']

    # Create a list of 66 0s for the LQs
    lqs = [0 for i in range(0,66)]

    # Determine LQs
    if lq_type == 'employees':
        localdenominator = localtotalemp
        usdenominator = ustotalemp
    else:
        localdenominator = localtotalwages
        usdenominator = ustotalwages

    for dict in local:
        lqs[dict['IO']-1] = dict[lq_type] / localdenominator

    for dict in us:
        try:
            lqs[dict['IO']-1] /= dict[lq_type] / usdenominator
        except:
            pass

    # Add a 67th LQ equal to 1 for government employment
    lqs.append(1)

    # If an lq is greater than 1, correct it to 1
    # Make sure no lqs are less than 0
    for i in range(len(lqs)):
        if lqs[i] > 1:
            lqs[i] = 1
        elif lqs[i] < 0:
            lqs[i] = 0
        else:
            pass
    return [lqs, us, local]


# Return a list of lists of direct requirements for the given year, geo, and type
def determine_direct_requirements(geo='US', year=2015, lq_type='wages'):
    lqoutput = determine_LQs(geo, year, lq_type)
    lqs = lqoutput[0]
    us = lqoutput[1]
    local = lqoutput[2]
    direct_requirements = multiply_short(list_to_sublists(lqs, 67), raw_direct_requirements)

    # Create an empty list for US revenue per employee
    us_rev_per_emp = [0 for i in range(66)]
    counter = 0
    for i in us_rev_per_emp:
        try:
            us_rev_per_emp[counter] = industry_totals[counter] / us[counter]['employees']
        except:
            pass
        counter += 1
    return [direct_requirements, us, local, us_rev_per_emp]


# TODO:
#   check direct requirements--make sure they are shares
def impact(geo_direct_requirements, impact_input):
    # {'ID':' 111CA', 'Desc':'Farms',
    # 'direct_rev':233900, 'indirect_rev':3326, 'induced_rev':705,
    # 'direct_emp':2, 'indirect_emp':0.03326, 'induced_emp':0.00704964751762412,
    # 'direct_wage':46780, 'indirect_wage':432.38, 'induced_wage':105.75}
    final_output = [
                    {'ID':0, 'Desc':'',
                    'direct_rev':0, 'indirect_rev':0, 'induced_rev':0,
                    'direct_emp':0, 'indirect_emp':0, 'induced_emp':0,
                    'direct_wage':0, 'indirect_wage':0, 'induced_wage':0} for i in range(66)
                    ]
    counter = 1
    for i in final_output:
        i['ID'] = counter
        i['Desc'] = naicsmatch[counter-1]['desc']
        counter += 1

    # Create lists of 0s for our direct inputs
    direct_employment = [0 for i in range(66)]
    direct_wages = [0 for i in range(66)]
    direct_revenue = [0 for i in range(66)]

    # Change those values based on actual user input
    direct_employment[impact_input[0]-1] = impact_input[1][1][1]
    direct_wages[impact_input[0]-1] = impact_input[1][1][2]
    direct_revenue[impact_input[0]-1] = impact_input[1][1][3]

    # This is our US emp and wages for each IO
    us = geo_direct_requirements[1]

    # This is our local emp and wages for each IO
    local = geo_direct_requirements[2]

    # This is our rev/emp for the US
    us_rev_per_emp = geo_direct_requirements[3]

    # Get our direct requirements
    direct_requirements = geo_direct_requirements[0]

    # These are our type1 and type2 matrices
    # divide direct requirements by industry totals and subtract that from the identity matrix
    type_1_A = subtract_short(identity_matrix(67, 67), divide_short(direct_requirements, list_to_sublists(industry_totals, 67)))
    type_1_B = subtract_short(identity_matrix(67, 67), divide_short(direct_requirements, list_to_sublists(industry_totals, 67)))

    # We shorten type1--removing 1 row and 1 column so that is has the correct contents
    del type_1_A[:1]
    for i in type_1_A:
        del i[:1]

    # Our direct and indirect coefficients are the inverse of Type 1A
    direct_and_indirect = inv(numpy.array(type_1_A)).tolist()

    # Our indirect and induced coefficients are the inverse of Type 1B
    indirect_and_induced = inv(numpy.array(type_1_B)).tolist()

    # Remove PCE and labor income/purchases from direct_requiements
    direct_requirements_shorter = direct_requirements
    del direct_requirements_shorter[:1]
    for i in direct_requirements:
        del i[:1]

    # Turn our list of direct revenue into a matrix so we can positionally multiply it for our first round purchases
    direct_revenue_matrix = list_to_sublists(direct_revenue, 66)

    # Our first round purchases are the direct requirements multiplied by the direct revenue for each sector
    first_round_purchases = multiply_short(direct_revenue_matrix, direct_requirements_shorter)
    sum_of_purchases = list_of_sublists_to_list_of_sums(transpose(first_round_purchases))

    # Multiply our sum of purchases by our direct and indirect coefficients, get our indirect revenue
    direct_revenue_copy = [0 for i in range(66)]
    direct_revenue_copy[impact_input[0] - 1] = impact_input[1][1][3]
    direct_and_indirect_revenue = multiply_short(list_to_sublists(sum_of_purchases, 66), direct_and_indirect)
    indirect_revenue = list_of_sublists_to_list_of_sums(transpose(direct_and_indirect_revenue))
    indirect_revenue[impact_input[0] - 1] -= impact_input[1][1][3]

    # Add wages to our sum of purchases
    sum_of_purchases_longer = sum_of_purchases
    sum_of_purchases_longer.append(direct_wages[impact_input[0]-1])

    # Multiply our sum of purchases (including wages) by our indirect and induced coefficients, get our induced revenue
    indirect_and_induced_revenue = multiply_short(list_to_sublists(sum_of_purchases_longer, 67), indirect_and_induced)
    induced_revenue = list_of_sublists_to_list_of_sums(transpose(indirect_and_induced_revenue))
    del induced_revenue[:1]
    counter = 0
    for i in induced_revenue:
        i -= indirect_revenue[counter]
        counter += 1

    # Fill our final output direct emp, wages, and rev
    for i in final_output:
        if i['ID'] == impact_input[0]:
            i['direct_emp'] = impact_input[1][1][1]
            i['direct_wage'] = impact_input[1][1][2]
            i['direct_rev'] = impact_input[1][1][3]

    # Fill our final output with indirect and induced rev
    counter = 0
    for i in final_output:
        i['indirect_rev'] = indirect_revenue[i['ID']-1]
        i['indirect_emp'] = indirect_revenue[i['ID']-1] / us_rev_per_emp[counter]
        i['induced_rev'] = induced_revenue[i['ID']-1]
        i['induced_emp'] = induced_revenue[i['ID']-1] / us_rev_per_emp[counter]
        if local[counter]['wages'] == 0 or local[counter]['employees'] == 0:
            pass
        else:
            i['indirect_wage'] = i['indirect_emp'] * local[counter]['wages'] / local[counter]['employees']
            i['induced_wage'] = i['induced_emp'] * local[counter]['wages'] / local[counter]['employees']

        counter += 1


    # {'ID':' 111CA', 'Desc':'Farms',
    # 'direct_rev':233900, 'indirect_rev':3326, 'induced_rev':705,
    # 'direct_emp':2, 'indirect_emp':0.03326, 'induced_emp':0.00704964751762412,
    # 'direct_wage':46780, 'indirect_wage':432.38, 'induced_wage':105.75}
    return final_output


# Takes a complex user input and translates it to run through the impact model
def complex_impact(user_input=['Alabama', 2015, [111, 100, 5000000, 15000000], 'wages']):
    IO = match_naics_to_IO(user_input[2][0])
    final_user_input = [IO, [user_input[1], user_input[2], user_input[3]]]
    direct_requirements = determine_direct_requirements(user_input[0], user_input[1], user_input[3])
    return impact(geo_direct_requirements=direct_requirements, impact_input=final_user_input)


# Takes a simple input (geo, year, sector) and translates it to run through the impact model
def simple_impact(user_input=['Alabama', 2015, 1]):
    # pull emp, wages for that sector
    # revenue = industry output * LQ
    # run model with those as user inputs

    geo_direct_requirements = determine_direct_requirements(geo=user_input[0], year=user_input[1], lq_type='wages')

    # This is our local emp and wages for each IO
    local = geo_direct_requirements[2]

    # This is our rev/emp for the US
    us_rev_per_emp = geo_direct_requirements[3]

    final_user_input = [user_input[2],
                        [user_input[1],
                            [111,
                             local[user_input[2]-1]['employees'],
                             local[user_input[2]-1]['wages'],
                             local[user_input[2]-1]['employees'] * us_rev_per_emp[user_input[2]-1]
                             ],
                         'wages'
                         ]
                        ]
    return impact(geo_direct_requirements=geo_direct_requirements, impact_input=final_user_input)


print(simple_impact(['Alabama', 2015, 1]))
