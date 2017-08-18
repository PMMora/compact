from matrixtools import blank_matrix, \
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

from matches import naicsmatch, fipsmatch
from UStable import raw_direct_requirements, industry_totals

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
    def loop(NAICS):
        try:
            IO = [pair['IO'] for pair in match if pair['NAICS'] == NAICS][0]
            return IO
        except:
            NAICS = str(NAICS)
            try:
                NAICS = int(NAICS[:len(NAICS) - 1])
                loop(NAICS)
            except:
                raise ValueError('Invalid NAICS entered')
    loop(NAICS)


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

    localerrorlist = []
    userrorlist = []

    for io in local:
        for dic in naicsmatch:
            naics = dic['NAICS']
            if dic['IO'] == io['IO']:
                try:
                    io['employees'] += select_column_yield(conn, 'employees', fips, 5, naics, year)[0]
                    io['wages'] += select_column_yield(conn, 'wages', fips, 5, naics, year)[0]
                except:
                    localerrorlist.append(naics)

    for io in us:
        for dic in naicsmatch:
            naics = dic['NAICS']
            if dic['IO'] == io['IO']:
                try:
                    io['employees'] += select_column_yield(conn, 'employees', 'US', 5, naics, year)[0]
                    io['wages'] += select_column_yield(conn, 'wages', 'US', 5, naics, year)[0]
                except:
                    userrorlist.append(naics)

    localtotalemp = 0
    localtotalwages = 0
    ustotalemp = 0
    ustotalwages = 0

    for dict in local:
        localtotalemp += dict['employees']
        localtotalwages += dict['wages']
    for dict in us:
        ustotalemp += dict['employees']
        ustotalwages += dict['wages']

    lqs = [0 for i in range(0,66)]

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
def determine_direct_requirements(geo='US', year=2015, lq_type='wage'):
    lqoutput = determine_LQs(geo, year, lq_type)
    lqs = lqoutput[0]
    us = lqoutput[1]
    local = lqoutput[2]
    direct_requirements = multiply_short(list_to_sublists(lqs, 67), raw_direct_requirements)
    return [direct_requirements, us, local]


# TODO:
#   first round purchases
def impact(direct_requirements, impact_input):
    direct_requirements = direct_requirements[0]
    us = direct_requirements[1]
    local = direct_requirements[2]
    type_1_A = subtract_short(identity_matrix(67, 67), divide_short(direct_requirements, list_to_sublists(industry_totals, 67)))
    type_1_B = subtract_short(identity_matrix(67, 67), divide_short(direct_requirements, list_to_sublists(industry_totals, 67)))
    del type_1_B[:1]
    for i in type_1_B:
        del i[:1]
    direct_and_indirect = inv(numpy.array(type_1_B)).tolist()
    direct_indirect_and_induced = inv(numpy.array(type_1_A)).tolist()
    print(direct_and_indirect)
    print(direct_indirect_and_induced)

    # determine first round purchases
    # horizontal sum of first round purchases

    # mult sum by direct_and_indirect

    # mult sum by direct_indirect_and_induced

    # indirect reve = horizontal sum of direct_and_indirect

    # induced reve = horizontal sum of direct_indirect_and_induced - pos direct_and_indirect


# Takes a complex user input and translates it to run through the impact model
def complex_impact(user_input=['Alabama', 2015, [111, 0, 0, 0], 'wages']):
    IO = match_naics_to_IO(user_input[2][0])
    final_user_input = [IO, [user_input[1], user_input[2], user_input[3]]]
    direct_requirements = determine_direct_requirements(user_input[0], user_input[1], user_input[3])
    return impact(direct_requirements=direct_requirements, impact_input=final_user_input)


# Takes a simple input (geo, year, sector) and translates it to run through the impact model
# TODO:
#   based on emp, wages for selected sector, estimate revenue
def simple_impact(user_input=['US', 2015, 1]):
    # pull emp, wages for that sector
    # revenue = industry output * LQ
    # run model with those as user inputs
    impact()
    pass


complex_impact()