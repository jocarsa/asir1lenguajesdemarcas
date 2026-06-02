# pip3 install mysql-connector-python

import mysql.connector

# connect
db = mysql.connector.connect(
    host="localhost",
    user="usuario",
    password="password",
    database="basedatos"
)

cursor = db.cursor()

# query
cursor.execute("SELECT * FROM clientes")

# print rows
for row in cursor:
    print(row)