import os, sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(os.path.dirname(base_dir), 'db.sqlite3')
conn = sqlite3.connect(database)
def select_all_from_yield(conn):
    '''return all rows from yield table
        :param: conn is a connection to the database
    '''
    sql = ''' SELECT * FROM yield'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def select_all_from_area(conn):
    '''return all rows from yield table
        :param: conn is a connection to the database
    '''
    sql = ''' SELECT * FROM area'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

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
    return cur.fetchone()[0]

def get_area_name(conn, fips):
    '''return the name of an area based off the fips_id'''
    sql = '''SELECT name FROM area
                WHERE fips = '{}' '''.format(fips)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]
