import sqlite3, os

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

def create_area_row(conn, area_row):
    sql = ''' INSERT INTO area (fips, name) 
                VALUES (?,?) '''
    cur = conn.cursor()
    cur.execute(sql, area_row)
    return cur.lastrowid

def create_area_info():
    fips_name_dic = {
                    '01':'Alabama',
                    '02':'Alaska',
                    '04':'Arizona',
                    '05':'Arkansas',
                    '06':'California',
                    '08':'Colorado',
                    '09':'Connecticut',
                    '10':'Delaware',
                    '11':'District of Columbia',
                    '12':'Florida',
                    '13':'Georgia',
                    '15':'Hawaii',
                    '16':'Idaho',
                    '17':'Illinois',
                    '18':'Indiana',
                    '19':'Iowa',
                    '20':'Kansas',
                    '21':'Kentucky',
                    '22':'Louisiana',
                    '23':'Main',
                    '24':'Maryland',
                    '25':'Massachusetts',
                    '26':'Michigan',
                    '27':'Minnesota',
                    '28':'Mississippi',
                    '29':'Missouri',
                    '30':'Montana',
                    '31':'Nebraska',
                    '32':'Nevada',
                    '33':'New Hampshire',
                    '34':'New Jersey',
                    '35':'New Mexico',
                    '36':'New York',
                    '37':'North Carolina',
                    '38':'North Dakota',
                    '39':'Ohio',
                    '40':'Oklahoma',
                    '41':'Oregon',
                    '42':'Pennsylvania',
                    '72':'Puerto Rico',
                    '44':'Rhode Island',
                    '45':'South Carolina',
                    '46':'South Dakota',
                    '47':'Tennessee',
                    '48':'Texas',
                    '49':'Utah',
                    '50':'Vermont',
                    '51':'Virginia',
                    '78':'Virgin Islands',
                    '53':'Washington',
                    '54':'West Virginia',
                    '55':'Wisconsin',
                    '56':'Wyoming'}
    with conn:
        for key, value in fips_name_dic.items():
            info = [key, value]
            create_area_row(conn,info)

base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(os.path.dirname(base_dir), 'db.sqlite3')
conn = create_connection(database)
create_area_info()