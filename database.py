import mysql.connector
db=mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="snsdforever9",
    database="borrowingsystem")

cursor=db.cursor()

query="CREATE TABLE accountinfo (id VARCHAR(255), password VARCHAR(255))"
cursor.execute(query)
db.commit()

db.close()