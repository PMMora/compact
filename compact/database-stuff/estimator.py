import os, sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(os.path.dirname(base_dir), 'db.sqlite3')
conn = sqlite3.connect(database)

def get_non_disclosed_rows(conn):
    sql = '''SELECT fips_id, naics_id, year, establishments, description, employees, wages
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
        
        total_employees = 0
        total_wages = 0

        disc_employees = 0
        disc_wages = 0

        est_employees = 0
        est_wages = 0

        undisclosed_rows = 0

        totals = get_totals_of_non_disclosed_naics(conn, gen_naics, year, area)

        for line in totals:
            print(line)

        for line in totals:
            if line[3]==0 and line[4] == 0 and row[5]==0 and row[6]==0:
                #print('HIGHER LEVEL NAICS')
                #print("Row to be estimated",row)
                #print('Suppressed higher level naic',line)
                us_totals = get_us_totals(conn, gen_naics, year)

                for us_row in us_totals:
                 #   print('US total for high level naic',us_row)
                    estab_ratio = float(line[2]/us_row[2])
                    
                    total_employees = us_row[3]*estab_ratio
                    total_wages = us_row[4]*estab_ratio

                  #  print('estimated total employees + wages in area naic',[total_employees,total_wages])

                total_disclosed = get_totals_of_disclosed_rows(conn, gen_naics, year, area)

                for disclosed_row in total_disclosed:
                    if disclosed_row[3] == 0 and disclosed_row[4] == 0:
                        undisclosed_rows +=1

                    employees = disclosed_row[3]
                    wages = disclosed_row[4]

                    total_employees -= int(employees)
                    total_wages -= int(wages)

                est_employees = round((total_employees/undisclosed_rows))
                est_wages = round((total_wages/undisclosed_rows))

                #print([est_employees, est_wages])
            else:
                #print('LOWER LEVEL NAICS')
                #print(row)
                total_employees = int(line[3])
                total_wages = int(line[4])
                total_disclosed = get_totals_of_disclosed_rows(conn, gen_naics, year, area)
                #print('total',total_employees, total_wages)


                for disclosed_row in total_disclosed:
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
                
       # print('disclosed',disc_employees, disc_wages)
       # print('new total',total_employees, total_wages)
       # print('row count', undisclosed_rows)
       # print('estimate',est_employees, est_wages)
                #print([naics, year, area, est_wages, est_employees])
        #print([naics, year, area, est_employees, est_wages])
        #update_non_disclosed_row(conn, str(naics), str(year), str(area), str(est_wages), str(est_employees))