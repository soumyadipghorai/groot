import sqlite3 

connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()

command = """
CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)
"""

cursor.execute(command)
print('database created')

cursor.execute("""
    INSERT INTO users VALUES ('ghorai', '1234');
""")

connection.commit();