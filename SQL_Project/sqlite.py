import sqlite3

# connect to sqlite
connection = sqlite3.connect("student.db")

cursor = connection.cursor()

#create the table
table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

#Insert some more records
cursor.execute('''Insert Into STUDENT values('Suraj', 'Data Science', 'A', 90)''')

print("Inserted records are")
data = cursor.execite('''Select * from STUDENT''')
for row in data:
    print(row)
    
connection.close()