import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowing_system"
)


print("name/times/name_times/stuff")
command = input("SELECT YOUR COMMAND : ")
if command =="name":
    Name_borrower = input("borrower name : ")
    mycursor = db.cursor()
    sql = "SELECT stuff FROM borrow WHERE name = %s"
    mycursor.execute(sql,(Name_borrower,))
    myresult = mycursor.fetchall()
    print(len(myresult),end="")
    print(" times")
    num = len(myresult)
    string={}
    for i in range(num):
        string[i]=str(myresult[i][0])
        print(string[i])

elif command =="times":
    mycursor = db.cursor()
    sql = "SELECT stuff FROM borrow"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(len(myresult),end="")
    print(" times")


elif command == "Check_Date":
    mycursor = db.cursor()
    sql = "SELECT YEAR(date) FROM borrow"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(sql)
    print(type(sql))


    Date= input("Year/Month : ")
    if Date =="Year":
        Year = input("YEAR :")

elif command=="check_owner":
    Stuff_ID = input("stuff id : ")
    mycursor = db.cursor()
    stuff_sql = "SELECT first_name FROM owner WHERE nstda_code = %s"
    mycursor.execute(stuff_sql,(Stuff_ID,))
    stuff_myresult = mycursor.fetchall()
    owner_sql = "SELECT last_name FROM owner WHERE nstda_code = %s"
    mycursor.execute(owner_sql,(Stuff_ID,))
    owner_myresult = mycursor.fetchall()
    num = len(stuff_myresult)
    stuff_string={}
    owner_string={}
    for i in range(num):
        stuff_string[i]=str(stuff_myresult[i][0])
        owner_string[i]=str(owner_myresult[i][0])
        print(stuff_string[i],owner_string[i])
  

    

    

   
mycursor.execute("SELECT id FROM borrow")
myresult = mycursor.fetchall()
##for row in myresult: 
   ##print(row)
