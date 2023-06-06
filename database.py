import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowing_system"
)

mycursor = db.cursor()

#mycursor.execute("CREATE DATABASE borrowing_system")

#mycursor.execute("CREATE TABLE data (id varchar(255), name varchar(255), tel varchar(255), stuff varchar(255),date timestamp,owner VARCHAR(100))")

#query="ALTER TABLE data ADD owner VARCHAR(100)"
#mycursor.execute(query)
#db.commit()

sql = "DELETE FROM data WHERE id = 'null'"

mycursor.execute(sql)

db.commit()