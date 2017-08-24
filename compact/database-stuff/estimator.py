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
            WHERE naics_id = '{}' AND year = '{}' AND fips_id = '{}' and own_code ='5' '''.format(gen_naics, year, area)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchone()
    return rows

def get_totals_of_disclosed_rows(conn, gen_naics, year, area):
    sql = '''SELECT fips_id, naics_id, establishments, employees, wages, disclosure_code FROM yield
                WHERE naics_id LIKE '{}_' and year = {} and fips_id = '{}' and own_code='5' '''.format(gen_naics, year, area)
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
    rows = cur.fetchone()
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
        #Adjust gen_naics for those naics that are grouped into bunches
        if int(gen_naics) in [31,32,33]:
            gen_naics = '31-33'
        elif int(gen_naics) in [44,45]:
            gen_naics = '44-45'
        elif int(gen_naics) in [48,49]:
            gen_naics = '48-49'

        totals = get_totals_of_non_disclosed_naics(conn, gen_naics, year, area)

        #If the totals are undisclosed grab US totals and get employee and wage value based on establishment ratio
        if totals[3]==0 and totals[4]==0:
            us_totals = get_us_totals(conn, gen_naics, year)
            estab_ratio = float(row[3]/us_totals[2])      
            est_employees = us_totals[3]*estab_ratio
            est_wages = us_totals[4]*estab_ratio

        #If total is disclosed, subtract disclosed values and distribute remainder to undisclosed rows
        else:
            total_employees = totals[3]
            total_wages = totals[4]
            
            #If gen_naics was a group, go back and get the individual naics value
            if isinstance(gen_naics, str):
                gen_naics = row[1][:-1]

            total_disclosed = get_totals_of_disclosed_rows(conn, gen_naics, year, area)
            
            for disclosed_row in total_disclosed:

                if disclosed_row[5] == 'N':
                    undisclosed_rows +=1


                employees = disclosed_row[3]
                wages = disclosed_row[4]

                disc_employees += employees
                disc_wages += wages


                total_employees -= int(employees)
                total_wages -= int(wages)

            est_employees = round(total_employees/undisclosed_rows)
            est_wages = round(total_wages/undisclosed_rows)

        update_non_disclosed_row(conn, naics, year, area, est_wages, est_employees)
