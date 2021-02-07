import sqlite3

con = sqlite3.connect('top.db')
_dbContext = con.cursor()

_dbContext.execute("""CREATE TABLE IF NOT EXISTS snake_top 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    total INT
                    )""")


def in_top(name, total):
    _dbContext.execute(f"INSERT INTO snake_top (name, total) VALUES ('{name}','{total}')")
    con.commit()


def output_top():
    _dbContext.execute("SELECT name,total FROM snake_top ORDER BY total DESC")
    return _dbContext.fetchmany(10)
