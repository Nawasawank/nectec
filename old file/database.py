import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowingsystem"
)

mycursor = mydb.cursor()






mycursor.execute("CREATE TABLE data (sequence VARCHAR(255), id VARCHAR(255), name VARCHAR(255),tel VARCHAR(255), stuff VARCHAR(255),date timestamp,owner VARCHAR(255),qr VARCHAR(255),status VARCHAR(255))")

#mycursor.execute("CREATE DATABASE borrowing_system")

#mycursor.execute("SELECT * FROM owner WHERE nstda_code = '9000-001-0001-000001887' ")

#myresult = mycursor.fetchall()


#for result in myresult:
   # print(result)

#query="ALTER TABLE user ADD avaliable VARCHAR(100)"
#mycursor.execute(query)
#mydb.commit()

#sql = "DELETE FROM data WHERE id = '1103703686615'"

#mycursor.execute(sql)

#db.commit()

#sql = "UPDATE user SET avaliable = 'True'"
#mycursor.execute(sql)

#mydb.commit()
