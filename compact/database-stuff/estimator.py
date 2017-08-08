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
            if line[3]==0 or line[4] == 0:
                continue
            else:
                print('BEGIN NEW ENTRY')
                print(row)
                print(line)

                total_employees = int(line[3])
                total_wages = int(line[4])
                #print([total_employees, total_wages])
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

                print([disc_employees, disc_wages])
                print([total_employees,total_wages])
        print([naics, year, area, est_employees, est_wages])
    #update_non_disclosed_row(conn, str(naics), str(year), str(area), str(est_wages), str(est_employees))