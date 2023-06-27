from flask import Flask, render_template,request,flash,jsonify
import mysql.connector
import datetime
from datetime import  timedelta
import os

from pyzbar import pyzbar
from PIL import Image



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'snsdforever9'
app.config['MYSQL_DB'] = 'borrowingsystem'
app.secret_key = 'kf1234'


mydb = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/borrow', methods=['POST'])
def borrow():
    return render_template('borrow.html')

@app.route('/return', methods=['POST'])
def Return():
    return render_template('return.html')


@app.route('/successborrow', methods=['POST'])
def scan_qr_code():
    error_messages = []
    try :
        # Get the uploaded file from the form
        qr_code = request.files['qr_code']
        # Open the uploaded file
        image = Image.open(qr_code)

        # Convert the image to grayscale
        grayscale_image = image.convert('L')
        # Decode the QR code
        decoded_data = pyzbar.decode(grayscale_image)
    except:
        decoded_data = []
        error_messages.append("Insert Qr Code")

    # Extract the string data
    print(decoded_data)
    string_data = None
    check = True
    if len(decoded_data) > 0:
        string_data = decoded_data[0].data.decode('utf-8')
    else:
        check=False
    
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        tel = request.form['tel']
        day = request.form['day']
        ref = request.form['ref']

        mycursor=mydb.cursor()
        now = datetime.datetime.now()
        if len(id) != 6:
            error_messages.append("ID must be 6 numbers")
        if len(name) < 2:
            error_messages.append("Name must be at least 2 characters")
        if len(tel) != 10:
            error_messages.append("Your number must be 10 digits")

        
        #เชื่อมเจ้าของ
        owner_sql = "SELECT nstda_code FROM user"
        mycursor.execute(owner_sql)
        owner_myresult = mycursor.fetchall()
        count = 0
        num = len(owner_myresult)
        for i in range(num):
            if string_data==owner_myresult[i][0]:
                count = int(i)
        owner_sql = "SELECT last_name FROM user"
        mycursor.execute(owner_sql)
        owner_myresult = mycursor.fetchall()
        Owner = owner_myresult[count][0]

        #connect to stuff
        stuff_sql = "SELECT first_name FROM user"
        mycursor.execute(stuff_sql)
        stuff_myresult = mycursor.fetchall()
        Stuff = stuff_myresult[count][0]

        sql = "SELECT nstda_code FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        ##check = False
        num = len(myresult)
        for i in range(num):
            if string_data == str(myresult[i][0]):
                check = True


        #อัพเดทสถานะด้วยการเช้ครหัส
        sql = "SELECT nstda_code FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        num = len(myresult) 
        count = 0
        for i in range(num):
            if string_data==myresult[i][0]:
                count = i
        print(count)
        print(string_data)

       
        
        owner_sql = "SELECT avaliable FROM user WHERE nstda_code=%s"
        mycursor.execute(owner_sql,(string_data,))
        myresult = mycursor.fetchall()
        num =  len(myresult)
        if num==0:
            avaliable = "None"
        else:   
            avaliable = myresult

        
        #เช็คว่าชื่อยืมคืน
        namesql="SELECT name from data WHERE qr=%s"
        mycursor.execute(namesql,(string_data,))
        myresult = mycursor.fetchall()
        name_user=myresult

        #เช้คลำดับ
        sql = "SELECT id FROM data"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        num = len(myresult)
        sequence = num+1

        print(avaliable[0][0])
        #insert information
        if error_messages ==[]:
            if str(string_data)!="None":
                num=len(name_user)
                if avaliable[0][0] =="True":

                    checkoutdate = (now + timedelta(days=int(day))).strftime('%Y-%m-%d ')
                    print(checkoutdate)


                    nsql = "UPDATE user SET avaliable = 'False' WHERE nstda_code = %s"
                    mycursor.execute(nsql,(string_data,))
                    mydb.commit()
                    sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status,ref,checkout,day) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s)"
                    values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,"borrow",ref,checkoutdate,day)
                    mycursor.execute(sql, values)
                    mydb.commit()
                elif avaliable=="None":
                    error_messages.append("Your QR code is wrong")
                elif num==0:
                    nsql = "UPDATE user SET avaliable = 'False' WHERE nstda_code = %s"
                    mycursor.execute(nsql,(string_data,))
                    mydb.commit()
                    
                    checkoutdate = (now + timedelta(days=int(day))).strftime('%Y-%m-%d ')
                    print(checkoutdate)


                    nsql = "UPDATE user SET avaliable = 'False' WHERE nstda_code = %s"
                    mycursor.execute(nsql,(string_data,))
                    mydb.commit()
                    sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status,ref,checkout,day) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s)"
                    values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,"borrow",ref,checkoutdate,day)
                    mycursor.execute(sql, values)
                    mydb.commit()
                else:
                    error_messages.append("Not avaliable")
            
        if len(error_messages) > 0:
            for error in error_messages:
                flash(error)
            return render_template('borrow.html', messages=error_messages)
        
        
        return render_template('successborrow.html',newstuff=Stuff,newstrdata=string_data,newcheck = check)

@app.route('/successreturn', methods=['GET', 'POST'])
def successreturn():
    string_data = None
    error_messages = []
    Stuff = None  # Initialize with default value
    check = False  # Initialize with default value
    checknotalert = True
    
    try:
        error_messages = []
        # Get the uploaded file from the form
        qr_code = request.files['qr_code']
        # Open the uploaded file
        image = Image.open(qr_code)

        # Convert the image to grayscale
        grayscale_image = image.convert('L')
        # Decode the QR code
        decoded_data = pyzbar.decode(grayscale_image)
    except:
        decoded_data = []
        error_messages.append("Insert Qr Code")

    # Extract the string data
    if len(decoded_data) > 0:
        string_data = decoded_data[0].data.decode('utf-8')

    if request.method == 'POST':
        id = request.form['id']
        ref = request.form['ref']
        mycursor = mydb.cursor()
        now = datetime.datetime.now()

        if len(id) != 6:
            error_messages.append("ID must be 6 numbers")

        # เชื่อมเจ้าของ
        owner_sql = "SELECT nstda_code FROM user"
        mycursor.execute(owner_sql)
        owner_myresult = mycursor.fetchall()
        count = 0
        num = len(owner_myresult)
        for i in range(num):
            if string_data == owner_myresult[i][0]:
                count = int(i)
        owner_sql = "SELECT last_name FROM user"
        mycursor.execute(owner_sql)
        owner_myresult = mycursor.fetchall()
        Owner = owner_myresult[count][0]

        # connect to stuff
        stuff_sql = "SELECT first_name FROM user"
        mycursor.execute(stuff_sql)
        stuff_myresult = mycursor.fetchall()
        Stuff = stuff_myresult[count][0]

        sql = "SELECT nstda_code FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        check = False
        num = len(myresult)
        for i in range(num):
            if string_data == str(myresult[i][0]):
                check = True
                break

        # อัพเดทสถานะด้วยการเช้ครหัส
        sql = "SELECT nstda_code FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        num = len(myresult)
        count = 0
        for i in range(num):
            if string_data == myresult[i][0]:
                count = i

        owner_sql = "SELECT avaliable FROM user WHERE nstda_code=%s"
        mycursor.execute(owner_sql, (string_data,))
        myresult = mycursor.fetchall()
        num = len(myresult)
        if num == 0:
            avaliable = "None"
        else:
            avaliable = myresult

        # เช็คว่าชื่อยืมคืน
        namesql = "SELECT name from data WHERE qr=%s"
        mycursor.execute(namesql, (string_data,))
        myresult = mycursor.fetchall()
        name_user = myresult

        # เช้คลำดับ
        sql = "SELECT id FROM data"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        num = len(myresult)
        sequence = num + 1

        # checkid
        namesql = "SELECT id from data WHERE qr=%s"
        mycursor.execute(namesql, (string_data,))
        myresult = mycursor.fetchall()
        id_user = myresult

        
        if avaliable != "None":
            num = len(name_user)
            if avaliable[0][0] == "False":
                checknotalert=True
                if id_user[-1][0] == id and len(id) == 6:
                    
                    daysql = "SELECT day FROM data WHERE qr LIKE %s AND status LIKE 'borrow' ORDER BY date DESC LIMIT 1"
                    mycursor = mydb.cursor()
                    mycursor.execute(daysql, (string_data,))
                    day = mycursor.fetchall()
                    day = day[0][0]

                    outsql = "SELECT checkout FROM data WHERE qr LIKE %s AND status LIKE 'borrow' ORDER BY date DESC LIMIT 1"
                    mycursor = mydb.cursor()
                    mycursor.execute(outsql, (string_data,))
                    checkout = mycursor.fetchall()
                    checkout = checkout[0][0]
                    #print(checkout)

                    sql = """SELECT name, id, tel, stuff FROM data WHERE qr LIKE %s AND status LIKE 'borrow'
                          AND date = (SELECT MAX(date) FROM data WHERE qr LIKE %s AND status LIKE 'borrow') LIMIT 1 """
                    mycursor = mydb.cursor()
                    mycursor.execute(sql, (string_data, string_data))
                    result = mycursor.fetchall()

                    if result:
                        name, id, tel, stuff = result[0]
                    else:
                        name = "Unknown"
                        id = "Unknown"
                        tel = "Unknown"
                        stuff = "Unknown"

                    insert_sql = """INSERT INTO data (sequence, id, name, stuff, tel, date, qr, owner, status, ref)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (sequence, id, name, stuff, tel, now.strftime('%Y-%m-%d %H:%M:%S'), string_data, Owner, "return", ref)
                    mycursor.execute(insert_sql, values)
                    mydb.commit()


                    sql = "UPDATE user SET avaliable = 'True' WHERE nstda_code = %s"
                    mycursor.execute(sql, (string_data,))
                    mydb.commit()

                    now = datetime.datetime.now()
                    now_str = now.strftime('%Y-%m-%d')  # Convert datetime object to string

                    if day is not None:
                        try:
    
                            day_int = int(day)
                            future_date = (now + timedelta(days=day_int)).strftime('%Y-%m-%d')
                            print(now_str)
                            print(future_date)
                            if future_date <= now_str:
                                checknotalert = False
                                warn = "Late Return"
                                alertt="Do you want to borrow"+stuff+"?"
                                return render_template('return.html', warn=warn, newstuff=Stuff, newstrdata=string_data, newcheck=check,alertt=alertt)
                            else:
                                alertt = "Do you want to borrow"+stuff+"?"
                                return render_template('return.html', alertt=alertt, newstuff=Stuff, newstrdata=string_data, newcheck=check)
                                
                           
                        except ValueError:
                            warn = "Invalid day value"

                elif avaliable == []:
                    check = False
                else:
                    if len(id_user) == 0:
                        error_messages.append("have nothing to return")
                    else:
                        error_messages.append("incorrect id")
            else:
                error_messages.append("have nothing to return")

        if len(error_messages) > 0:
            for error in error_messages:
                flash(error)
            return render_template('return.html', messages=error_messages)
        
        if(checknotalert!=True):
            return render_template('successreturn.html', newstuff=Stuff, newstrdata=string_data, newcheck=check)
        
    return render_template('successreturn.html', newstuff=Stuff, newstrdata=string_data, newcheck="notalert")


@app.route('/history', methods=['GET','POST'])
def history():
    return render_template('history.html')

@app.route('/userrecord', methods=['GET', 'POST'])
def userrecord():
    return render_template('userrecord.html')

@app.route('/overview', methods=['GET', 'POST'])
def overview():
    return render_template('overview.html')

@app.route('/accessinformation', methods=['GET', 'POST'])
def accessinformation():
    return render_template('accessinformation.html')

@app.route('/notreturnstuff', methods=['GET', 'POST'])
def notreturnstuff():
    return render_template('notreturnstuff.html')

@app.route('/checkdate', methods=['GET', 'POST'])
def checkdate():
    return render_template('checkdate.html')

@app.route('/chart', methods=['GET', 'POST'])
def chartperyear():
    return render_template('chart.html')


#findall users record
@app.route('/allborrow', methods=['GET','POST'])
def alldataborrow():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )

    mycursor = mydb.cursor()
    sql = "SELECT * FROM data"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
 
    data_list = []
    for x in myresult:
        data = {
            "sequence": x[0],
            "id": x[1],
            "name": x[2],
            "tel": x[3],
            "stuff": x[4],
            "date": x[5],
            "owner": x[6],
            "qr": x[7],
            "status" : x[8]
        }
        data_list.append(data)

    return jsonify(data_list)

#borrowing information
@app.route('/borrowdata', methods=['POST'])
def borrowdata():
    allData = request.json
    date = allData['date']
    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE status = 'borrow' AND  DATE(date) = '"+date+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    data_list = []
    for x in myresult:
        data = {
            "sequence": x[0],
            "id": x[1],
            "name": x[2],
            "tel": x[3],
            "stuff": x[4],
            "date": x[5],
            "owner": x[6],
            "qr": x[7]
        }
        data_list.append(data)

    return jsonify(data_list)


#return information
@app.route('/returndata', methods=['POST'])
def returndata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )

    allData = request.json
    date = allData['date']
    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE status = 'return' AND  DATE(date) = '"+date+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    data_list = []
    for x in myresult:
        data = {
            "sequence": x[0],
            "id": x[1],
            "name": x[2],
            "tel": x[3],
            "stuff": x[4],
            "date": x[5],
            "owner": x[6],
            "qr": x[7]
        }
        data_list.append(data)

    return jsonify(data_list)

#collect data who not return
#collect data who not return
@app.route('/notreturn', methods=['POST'])
def notreturn():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )
    borrow_sql = "SELECT stuff FROM data WHERE status LIKE 'borrow'"
    mycursor = mydb.cursor()
    mycursor.execute(borrow_sql,)
    result = mycursor.fetchall()
    return_sql = "SELECT stuff FROM data WHERE status LIKE 'return'"
    mycursor = mydb.cursor()
    mycursor.execute(return_sql,)
    myresult = mycursor.fetchall()
    dict_borrow = {}
    dict_return = {}
    num_borrow = len(result)
    num_return = len(myresult)
    
    for i in range(num_borrow):
        dict_borrow[result[i][0]] = 0
        dict_return[result[i][0]] = 0

    for i in range(num_borrow):
        if not result[i][0] in dict_borrow:
            dict_borrow[result[i][0]] = 0
        else:
            dict_borrow[result[i][0]] += 1

    for i in range(num_return):
        if not myresult[i][0] in dict_return:
            dict_return[myresult[i][0]] = 0
        else:
            dict_return[myresult[i][0]] += 1

    list_not_returned = []
    for i in range(num_borrow):
        if not dict_borrow[result[i][0]] == dict_return[result[i][0]]:
            if not result[i][0] in list_not_returned:
                list_not_returned.append(result[i][0])

    num_not_returned = len(list_not_returned)
    print(list_not_returned)
    data_list = []

    for i in range(num_not_returned):
        all_sql = "SELECT * FROM data WHERE stuff = %s AND status LIKE 'borrow' ORDER BY date DESC LIMIT 1" 
        mycursor.execute(all_sql, (list_not_returned[i],))
        inner_result = mycursor.fetchall()
    
        for x in inner_result:
            currentTime = datetime.datetime.now();
            if x[10] < str(currentTime):
                Check = False
            else:
                Check = True
            
            data = {
                "sequence": x[0],
                "id": x[1],
                "name": x[2],
                "tel": x[3],
                "stuff": x[4],
                "date": x[5],
                "owner": x[6],
                "qr": x[7],
                "ref": x[9],
                "day": x[10],
                "check": Check
                }
            data_list.append(data)
            print(x[10])
            print(currentTime)
            print(Check)
            

    return jsonify(data_list)

@app.route('/qrdata', methods=['POST'])
def qrdata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )
    allData = request.json
    qr = allData['qrData']
    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE qr = '"+qr+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    data_list = []
    if myresult:
        for x in myresult:
            data = {
                "sequence": x[0],
                "id": x[1],
                "name": x[2],
                "tel": x[3],
                "stuff": x[4],
                "date": x[5],
                "owner": x[6],
                "qr": x[7]
            }
            data_list.append(data)

    return jsonify(data_list)

@app.route('/returnyear', methods=['POST'])
def returnyear():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mingming260947",
        database="borrowingsystem"
    )
    allData = request.json
    year = allData['year']
    option = allData['option']
    mycursor = mydb.cursor()

    if option=="return":
        sql = "SELECT * FROM data WHERE YEAR(date) LIKE %s AND status = 'return' "
        mycursor.execute(sql, (year,))
        myresult = mycursor.fetchall()
        data_list = []
        for x in myresult:
            data = {
                "sequence": x[0],
                "id": x[1],
                "name": x[2],
                "tel": x[3],
                "stuff": x[4],
                "date": x[5],
                "owner": x[6],
                "qr": x[7]
            }
            data_list.append(data)

        return jsonify(data_list)
    else:
        sql = "SELECT * FROM data WHERE YEAR(date) LIKE %s AND status = 'borrow'"
        mycursor.execute(sql, (year,))
        myresult = mycursor.fetchall()
        data_list = []
        for x in myresult:
            data = {
                "sequence": x[0],
                "id": x[1],
                "name": x[2],
                "tel": x[3],
                "stuff": x[4],
                "date": x[5],
                "owner": x[6],
                "qr": x[7]
            }
            data_list.append(data)

        return jsonify(data_list)
    
@app.route('/returnmonth', methods=['POST'])
def returnmonth():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )
    allData = request.json
    year = allData['year']
    month = allData['month']
    option = allData['option']
    mycursor = mydb.cursor()
    #sql = "SELECT * FROM data WHERE DATE(date) LIKE %s"
    #mycursor.execute(sql, (date,))
    if option=="return":
        sql = "SELECT * FROM data WHERE YEAR(date) LIKE %s AND MONTH(date) LIKE %s AND status = 'return' "
        mycursor.execute(sql, (year,month,))
        myresult = mycursor.fetchall()
        data_list = []
        for x in myresult:
            data = {
                "sequence": x[0],
                "id": x[1],
                "name": x[2],
                "tel": x[3],
                "stuff": x[4],
                "date": x[5],
                "owner": x[6],
                "qr": x[7]
            }
            data_list.append(data)


        return jsonify(data_list)
    else:
        sql = "SELECT * FROM data WHERE YEAR(date) = %s AND MONTH(date) = %s AND status = 'borrow'"
        mycursor.execute(sql, (year,month,))
        myresult = mycursor.fetchall()
        data_list = []
        for x in myresult:
            data = {
                "sequence": x[0],
                "id": x[1],
                "name": x[2],
                "tel": x[3],
                "stuff": x[4],
                "date": x[5],
                "owner": x[6],
                "qr": x[7]
            }
            data_list.append(data)

        return jsonify(data_list)

@app.route('/chartborrow', methods=['POST'])
def chartborrow():
    mycursor = mydb.cursor()
    data_list = []
    allData = request.json
    year = allData['year']
    for month in range(1, 13):
        sql = "SELECT COUNT(*) AS times FROM data WHERE YEAR(date) = %s AND MONTH(date) = %s AND status = 'borrow'"
        mycursor.execute(sql, (year,month,))
        result = mycursor.fetchone()
        times = result[0]

        data = {
            "month": month,
            "times": times
        }
        data_list.append(data)

    return jsonify(data_list)

@app.route('/chartreturn', methods=['POST'])
def chartreturn():

    allData = request.json
    year = allData['year']

    mycursor = mydb.cursor()
    data_list = []

    for month in range(1, 13):
        sql = "SELECT COUNT(*) AS times FROM data WHERE YEAR(date) = %s AND MONTH(date) = %s AND status = 'return'"
        mycursor.execute(sql,(year,month,))
        result = mycursor.fetchone()
        times = result[0]

        data = {
            "month": month,
            "times": times
        }
        data_list.append(data)

    return jsonify(data_list)

@app.route('/accessinfor', methods=['GET', 'POST'])
def accessinfor():
    if request.method == 'POST':
        error_messages = []
        error=[]
        try:
            # Get the uploaded file from the form
            qr_code = request.files['qr_code']
            # Open the uploaded file
            image = Image.open(qr_code)

            # Convert the image to grayscale
            grayscale_image = image.convert('L')
            # Decode the QR code
            decoded_data = pyzbar.decode(grayscale_image)
        except:
            decoded_data = []

        if decoded_data:
            # Extract the string data
            string_data = decoded_data[0].data.decode('utf-8')
            mycursor = mydb.cursor()

            sql = "SELECT * from data WHERE qr=%s"
            mycursor.execute(sql, (string_data,))
            myresult = mycursor.fetchall()
            print(myresult)

            nsql = "SELECT first_name from user WHERE nstda_code=%s"
            mycursor.execute(nsql, (string_data,))
            ownresult = mycursor.fetchall()
            namestuff = "Stuff: " + str(ownresult[0][0]) if ownresult else "Stuff: Not Found"

            osql = "SELECT last_name from user WHERE nstda_code=%s"
            mycursor.execute(osql, (string_data,))
            stuffresult = mycursor.fetchall()
            nameowner = "Owner: " + str(stuffresult[0][0]) if stuffresult else "Owner: Not Found"
            print(nameowner)

            if myresult == []:
                error_messages.append("No data found")

            data_list = []
            for x in myresult:
                data = {
                    "sequence": x[0],
                    "id": x[1],
                    "name": x[2],
                    "tel": x[3],
                    "stuff": x[4],
                    "date": x[5],
                    "owner": x[6],
                    "qr": x[7],
                    "status": x[8]
                }
                data_list.append(data)

            if error_messages:
                return render_template('accessinformation.html', messages=error_messages,messages2=error)
            else:
                return render_template('accessinformation.html', data_list=data_list, stuff=namestuff, owner=nameowner,messages2=error)
        else:
            error.append("No QR Code")
            return render_template('accessinformation.html', messages2=error)

    return render_template('accessinformation.html', messages=error_messages,messages2=error)

    
if __name__ == "__main__":
    app.run (host = os.getenv('IP', "0.0.0.0"),
            port = int(os.getenv('PORT',4444)))