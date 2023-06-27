import mysql.connector
db=mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="snsdforever9",
    database="borrowingsystem")

cursor=db.cursor()

query="DELETE FROM data WHERE id = '333333'"
cursor.execute(query)
db.commit()

db.close()