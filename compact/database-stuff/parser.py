import os, csv, sqlite3

def get_header_index(file):
    fips = 'area_fips'
    naics = 'industry_code'
    year = 'year'
    disclosure_code = 'disclosure_code'
    establishments = 'annual_avg_estabs'
    employees = 'annual_avg_emplvl'
    wages = 'total_annual_wages'
    input_list = [fips, naics, year, disclosure_code, establishments,employees,wages]
    with open(file, newline='\n') as f:
        reader = csv.reader(f)
        row1 = next(reader)
        indexes = []
        for item in input_list:
            if item in row1:
                indexes.append(row1.index(item))
        return indexes

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None

def create_yield_row(conn, yield_row):
    sql = ''' INSERT INTO yield (fips_id, naics_id, year, disclosure_code, establishments, employees, wages)
                VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, yield_row)
    return cur.lastrowid

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "CSV_files/01000.csv")
    database = os.path.join(os.path.dirname(base_dir), 'db.sqlite3')
    conn = create_connection(database)
    with conn:
        with open(csv_file, newline='\n') as f:
            reader = csv.reader(f)
            indexes = get_header_index(csv_file)
            for row in reader:
                info = []
                for i in indexes:
                    if i == 2:
                        if len(row[i]) == 3 or len(row[i]) == 6:
                            info.append(row[i])
                        else:
                            info = []
                            break
                    else:
                        info.append(row[i])
                if info:
                    print(info)
                    create_yield_row(conn, info)
                


main()