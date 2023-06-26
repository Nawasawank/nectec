import mysql.connector
import datetime
from flask import request

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowingsystem"
)



def insert_data(name, id,tel, string_data, Owner):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowingsystem")

    now = datetime.datetime.now()
    mycursor = mydb.cursor()
    # Execute the query to get the existing records
    sql = "SELECT id FROM data"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    num = len(myresult)
    sequence = num + 1

    #connect stuff
    owner_sql = "SELECT nstda_code FROM user"
    mycursor.execute(owner_sql)
    owner_myresult = mycursor.fetchall()
    count = 0
    num = len(owner_myresult)
    for i in range(num):
        if string_data==owner_myresult[i][0]:
            count = int(i)
    stuff_sql = "SELECT first_name FROM user"
    mycursor.execute(stuff_sql)
    stuff_myresult = mycursor.fetchall()
    stuff = stuff_myresult[count][0]
    

    # Insert new data into the table
    sql = "INSERT INTO data (sequence, id, name, stuff, tel, date, qr, owner, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (sequence, id, name, stuff, tel, now.strftime('%Y-%m-%d %H:%M:%S'), string_data, Owner, "borrow")
    mycursor.execute(sql, values)
    mydb.commit()

    mycursor.close()
    mydb.close()

def output_data(string_data):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowingsystem")
    
    now = datetime.datetime.now()
    mycursor = mydb.cursor()
    # Execute the query to get the existing records
    sql = "SELECT id FROM data"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    num = len(myresult)
    sequence = num + 1

    sql = "SELECT name FROM data WHERE qr = %s"
    mycursor.execute(sql,(string_data,))
    myresult = mycursor.fetchall()
    name = myresult[-1][0]
    print(name)

    sql = "SELECT id FROM data WHERE qr = %s"
    mycursor.execute(sql,(string_data,))
    myresult = mycursor.fetchall()
    id = myresult[-1][0]

    sql = "SELECT tel FROM data WHERE qr = %s"
    mycursor.execute(sql,(string_data,))
    myresult = mycursor.fetchall()
    tel = myresult[-1][0]

    sql = "SELECT stuff FROM data WHERE qr = %s"
    mycursor.execute(sql,(string_data,))
    myresult = mycursor.fetchall()
    stuff = myresult[-1][0]

    sql = "SELECT owner FROM data WHERE qr = %s"
    mycursor.execute(sql,(string_data,))
    myresult = mycursor.fetchall()
    Owner = myresult[-1][0]

    # Insert new data into the table
    sql = "INSERT INTO data (sequence, id, name, stuff, tel, date, qr, owner, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (sequence, id, name, stuff, tel, now.strftime('%Y-%m-%d %H:%M:%S'), string_data, Owner, "return")
    mycursor.execute(sql, values)
    mydb.commit()

    mycursor.close()
    mydb.close()

def alldata():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowingsystem")

    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE status = 'borrow' "
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) > 0: 
        for x in myresult:
            arr = {
                "sequence" : x[0],
                "id" : x[1],
                "name" : (x[2]),
                "tel" : x[3],
                "stuff" : x[4],
                "date" : x[5],
                "owner" : x[6],
                "qr" : x[7]
                }
    return arr