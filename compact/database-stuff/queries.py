import os, sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(os.path.dirname(base_dir), 'db.sqlite3')

def select_all_from_yield():
	conn = sqlite3.connect(database)
	sql = ''' SELECT * FROM yield'''
	cur = conn.cursor()
	cur.execute(sql)

	rows = cur.fetchall()

	for row in rows:
		print(row)
	return rows

select_all_from_yield()