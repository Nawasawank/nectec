import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="borrowingsystem"
)
print("Command typing:\nUser record : ur\nOverview of the year : ooty\nBorrowing record : br\nReturn record : rr\nCheck stuff owner : cso\nNot return stuff : nrs")

#เช็คว่าคนนี้ยืมคืนอะไรไปบ้างกี่ครั้ง
print("-------------------------------------------------")
command = input("SELECT YOUR COMMAND : ")
print("-------------------------------------------------")
if command =="ur":
    Name_borrower = input("borrower name : ")
    mycursor = db.cursor()
    sql_stuff= "SELECT stuff FROM data WHERE name = %s"
    mycursor.execute(sql_stuff,(Name_borrower,))
    stuffresult = mycursor.fetchall()
        
    sql_date= "SELECT date FROM data WHERE name = %s"
    mycursor.execute(sql_date,(Name_borrower,))
    dateresult = mycursor.fetchall()

    sql_status= "SELECT status FROM data WHERE name = %s"
    mycursor.execute(sql_status,(Name_borrower,))
    statusresult = mycursor.fetchall()

    sql_check= "SELECT status FROM data WHERE status='borrow' AND name=%s"
    mycursor.execute(sql_check,(Name_borrower,))
    checkresult = mycursor.fetchall()
    num = len(checkresult)
    num_all = len(stuffresult)
    num_return = num_all-num
    print(num_all,end="")
    print(" times")
    print("borrow: "+str(num)+' times  '+"return: "+str(num_return)+' times')
    print()
    num = len(stuffresult)
    string={}
    for i in range(num):
        print(str(statusresult[i][0])+" "+str(dateresult[i][0])+"\n"+str(stuffresult[i][0]))       
        print()
    print("-------------------------------------------------")


#เช็คทั้งปีว่าของถูกยืมไปทั้งหมดกี่ครั้ง  
elif command == "ooty":
    year = input("Year: ")
    mycursor = db.cursor()
    sql = "SELECT date FROM data WHERE status LIKE 'borrow'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    num = len(myresult)
    
    sql = "SELECT stuff FROM data WHERE date like %s AND status LIKE 'borrow'"
    mycursor.execute(sql,('%' + year+ '%',))
    result = mycursor.fetchall()
    num = len(myresult)
    dict = {}
    #print(result)
    for i in range(num):
        if not result[i][0] in dict:
            dict[result[i][0]]=1
        else:
            dict[result[i][0]]+=1
    for key,value in dict.items():
        print(key,value,"times")
    print("-------------------------------------------------")

#วัน-เดือน-ปีมีใครยืมอะไรไปบ้าง
elif command == "br":
    Year = input("Year: ")
    Month = input("Month: ")
    Date = input("Date: ")
    y_m_d = Year+"-"+Month+"-"+Date
    sql = "SELECT stuff, name FROM data WHERE date LIKE %s AND status LIKE 'borrow'"
    mycursor = db.cursor()
    mycursor.execute(sql, ('%' + y_m_d + '%',))
    result = mycursor.fetchall()
    result_str = ""
    for row in result:
        result_str += f"{row[0]} - {row[1]}\n\n"
    print("")
    print(y_m_d)
    print()
    print(result_str)
    print("-------------------------------------------------")

#วัน-เดือน-ปีมีใครคืนอะไรไปบ้าง
elif command == "rr":
    Year = input("Year: ")
    Month = input("Month: ")
    Date = input("Date: ")
    y_m_d = Year+"-"+Month+"-"+Date
    sql = "SELECT stuff, name FROM data WHERE date LIKE %s AND status LIKE 'return'"
    mycursor = db.cursor()
    mycursor.execute(sql, ('%' + y_m_d + '%',))
    result = mycursor.fetchall()
    result_str = ""
    for row in result:
        result_str += f"{row[0]} - {row[1]}\n\n"
    print("")
    print(y_m_d)
    print()
    print(result_str)
    print("-------------------------------------------------")

#เช็คstuff id ใครเป็นเจ้าของของอะไร
elif command=="cso":
    Stuff_ID = input("stuff id : ")
    mycursor = db.cursor()
    stuff_sql = "SELECT first_name FROM user WHERE nstda_code = %s"
    mycursor.execute(stuff_sql,(Stuff_ID,))
    stuff_myresult = mycursor.fetchall()
    owner_sql = "SELECT last_name FROM user WHERE nstda_code = %s"
    mycursor.execute(owner_sql,(Stuff_ID,))
    owner_myresult = mycursor.fetchall()
    num = len(stuff_myresult)
    stuff_string={}
    owner_string={}
    for i in range(num):
        stuff_string[i]=str(stuff_myresult[i][0])
        owner_string[i]=str(owner_myresult[i][0])
        print(stuff_string[i],owner_string[i])
    print("-------------------------------------------------")

#เช็คว่าใครยังไม่คืนบ้าง
elif command =="nrs":

    #เช้คตัวreturn ว่ามีกี่ตัว borrowว่ามีกี่ตัว ถ้าไม่เท่ากันคือยังไม่ได้คืน

    borrow_sql = "SELECT stuff FROM data WHERE status LIKE 'borrow'"
    mycursor = db.cursor()
    mycursor.execute(borrow_sql,)
    result = mycursor.fetchall()
    return_sql = "SELECT stuff FROM data WHERE status LIKE 'return'"
    mycursor = db.cursor()
    mycursor.execute(return_sql,)
    myresult = mycursor.fetchall()
    dict_borrow={}
    dict_return={}
    num_borrow = len(result)
    num_return = len(myresult)
    for i in range(num_borrow):
        #print(result[i][0])
        #print(type(result[i][0]))
        dict_borrow[result[i][0]]=0
        dict_return[result[i][0]]=0

    for i in range(num_borrow):
        if not result[i][0] in dict_borrow:
            dict_borrow[result[i][0]]=0
        else:
            dict_borrow[result[i][0]]+=1
    for i in range(num_return):
        if not myresult[i][0] in dict_return:
            dict_return[myresult[i][0]]=0
        else:
            dict_return[myresult[i][0]]+=1

    list =[]
    for i in range(num_borrow):
        if not dict_borrow[result[i][0]]==dict_return[result[i][0]]:
            if not result[i][0] in list:
                list.append(result[i][0])
    num = len(list)
    for i in range(num):
        namesql = "SELECT name FROM data WHERE stuff LIKE %s AND status LIKE 'borrow' ORDER BY sequence DESC LIMIT 1" 
        mycursor = db.cursor()
        mycursor.execute(namesql, (list[i],))
        myresult = mycursor.fetchall()
        print(int(i + 1), end=". ")
        print(list[i] + "\nborrow by: ", end="")
        for row in myresult:
            print(row[0])
        print("-------------------------------------------------")
