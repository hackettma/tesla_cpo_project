import sqlite3 as lite

con = lite.connect('temp.db', detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES)
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Cars")
	cur.execute("CREATE TABLE Cars(Id TEXT, Created_at timestamp, Last_Update timestamp, Status TEXT, Location TEXT, Year TEXT, Model TEXT, Mileage FLOAT, Price FLOAT, Paint TEXT, Interior TEXT, Roof TEXT, Wheel TEXT)")