import os, sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(os.path.dirname(base_dir), 'testdb.sqlite3')
conn = sqlite3.connect(database)

def get_non_disclosed_rows(conn):
    sql = '''SELECT fips_id, naics_id, year, establishments, description
                FROM yield JOIN industry ON naics = naics_id
                WHERE disclosure_code = 'N' AND own_code = '5' '''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def get_totals_of_non_disclosed_naics(conn, gen_naics, year, area):
    sql = '''SELECT fips_id, naics_id, establishments, employees, wages FROM yield
            WHERE naics_id = {} AND year = {} AND fips_id = {} and own_code ='5' '''.format(gen_naics, year, area)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def get_totals_of_disclosed_rows(conn, gen_naics, year, area):
    sql = '''SELECT fips_id, naics_id, establishments, employees, wages FROM yield
                WHERE naics_id LIKE '{}_' and year = {} and fips_id = {} and own_code='5' '''.format(gen_naics, year, area)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def update_non_disclosed_row(conn, naics, year, area, wages, employees):
    sql = '''UPDATE yield
                SET wages = ?, employees = ?
                WHERE naics_id = ? AND year = ? AND fips_id = ? and own_code = '5' '''
    cur = conn.cursor()
    cur.execute(sql,(wages, employees, naics, year, area))

def get_us_totals(conn, naics, year):
    sql = '''SELECT fips_id, naics_id, establishments, employees, wages FROM yield
            WHERE naics_id = {} and year = {} and fips_id = 'US' and own_code = '5' '''.format(naics, year)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

suppressed = get_non_disclosed_rows(conn)

with conn:
    for row in suppressed:
        naics = row[1]
        gen_naics = row[1][:-1]
        year = row[2]
        area = row[0]
        totals = get_totals_of_non_disclosed_naics(conn, gen_naics, year, area)

        est_employees=0
        est_wages=0

        for line in totals:
            if line[3]==0 and line[4] == 0:
                print('New Row')
                print(row)
                print(line)
                us_totals = get_us_totals(conn, gen_naics, year)
                for us_row in us_totals:
                    print(us_row)
                    estab_ratio = float(line[2]/us_row[2])
                    
                    new_total_emp = us_row[3]*estab_ratio
                    new_total_wage = us_row[4]*estab_ratio

                    total_disclosed = get_totals_of_disclosed_rows(conn, gen_naics, year, area)

                    for discclosed_row in total_disclosed:
                        print(discclosed_row)

                    '''disc_employees = 0
                    disc_wages =0
                    undisclosed_rows = 0
                    for disclosed_row in total_disclosed[1:]:
                        if disclosed_row[3] == 0 and disclosed_row[4] ==0:
                            undisclosed_rows += 1

                        employees = disclosed_row[3]
                        wages = disclosed_row[4]

                        disc_employees += disclosed_row[3]
                        disc_wages += disclosed_row[4]


                        new_total_emp -= int(employees)
                        new_total_wage -= int(wages)

                    est_employees = round(new_total_emp/undisclosed_rows)
                    est_wages = round(new_total_wage/undisclosed_rows)

                    print([est_employees, est_wages])'''
            else:
                total_employees = int(line[3])
                total_wages = int(line[4])
                total_disclosed = get_totals_of_disclosed_rows(conn, gen_naics, year, area)

                undisclosed_rows = 0

                disc_employees = 0
                disc_wages =0

                for disclosed_row in total_disclosed[1:]:
                    if disclosed_row[3] == 0 and disclosed_row[4] ==0:
                        undisclosed_rows += 1

                    employees = disclosed_row[3]
                    wages = disclosed_row[4]

                    disc_employees += disclosed_row[3]
                    disc_wages += disclosed_row[4]


                    total_employees -= int(employees)
                    total_wages -= int(wages)

                est_employees = round(total_employees/undisclosed_rows)
                est_wages = round(total_wages/undisclosed_rows)

        #update_non_disclosed_row(conn, str(naics), str(year), str(area), str(est_wages), str(est_employees))