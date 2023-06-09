import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowing_system"
)

command = input("SELECT YOUR COMMAND : ")
if command=="check_owner":
    Stuff_ID = input("stuff id : ")
    mycursor = db.cursor()
    sql = "SELECT first_name FROM owner WHERE nstda_code = %s"
    mycursor.execute(sql,(Stuff_ID,))
    myresult = mycursor.fetchall()
    num = len(myresult)
    string={}
    for i in range(num):
        string[i]=str(myresult[i][0])
        print(string[i])