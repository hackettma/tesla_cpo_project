import sqlite3 as lite

con = lite.connect('C:/Users/michael.hackett/Documents/Personal/Selenium/temp.db', detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES)
cur = con.cursor()
temp_list = list(cur.execute("SELECT Id FROM Cars").fetchall())
for item in temp_list:
		print(item[0])