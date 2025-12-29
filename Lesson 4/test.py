import sqlite3
DB_PATH = "test.db"

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("SELECT name FROM people where id = 1;")
con.commit()
rows = cur.fetchall()
print(rows)