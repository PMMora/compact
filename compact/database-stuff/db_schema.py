'''
Run once to build the necessary tables in the db.sqlite3 database
'''

import sqlite3, os

def create_connection(db_file):
    ''' create a database connection to the SQLite database specified by db
        :param db: database file path
        Return the conn or None
	'''
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    '''Create a table from the create_table_sql statement
    :param conn: Connection object
    :parak create_table_sql: a CREATE TABLE statement
    '''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print("ERROR IN CREATING TABLE" + str(e))

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db = os.path.join(base_dir, 'db.sqlite3')

    sql_create_area_table = """ CREATE TABLE IF NOT EXISTS area (
                                fips text PRIMARY KEY,
                                name text
                               ); """
    sql_create_industry_table = """ CREATE TABLE IF NOT EXISTS industry (
                                naics text PRIMARY KEY,
                                bea_sector_id text,
                                description text
                                ); """
    sql_create_yield_table = """ CREATE TABLE IF NOT EXISTS yield (
                                fips_id text,
                                own_code text,
                                naics_id text,
                                year integer,
                                disclosure_code text,
                                establishments integer,
                                employees integer,
                                wages integer,
                                FOREIGN KEY (fips_id) REFERENCES area (fips),
                                FOREIGN KEY (naics_id) REFERENCES industry (naics)
                                ); """

    conn = create_connection(db)
    
    if conn is not None:
        create_table(conn, sql_create_area_table)
        create_table(conn, sql_create_industry_table)
        create_table(conn, sql_create_yield_table)

    else:
        print("Yo you messed up on the connection")

if __name__ == '__main__':
    main()