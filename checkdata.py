import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="newtest"
)


print("name/times/name_times/stuff")
command = input("SELECT YOUR COMMAND : ")
if command =="name":
    Name_borrower = input("borrower name : ")
    mycursor = db.cursor()
    sql = "SELECT stuff FROM data WHERE name = %s"
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
    sql = "SELECT stuff FROM data"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(len(myresult),end="")
    print(" times")


elif command == "Check_Date":
    mycursor = db.cursor()
    sql = "SELECT YEAR(date) FROM data"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(sql)
    print(type(sql))


    Date= input("Year/Month : ")
    if Date =="Year":
        Year = input("YEAR :")
    
  

    

    

   
mycursor.execute("SELECT id FROM data")
myresult = mycursor.fetchall()
##for row in myresult: 
   ##print(row)
