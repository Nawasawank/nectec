from flask import Flask, render_template, request, flash, jsonify, session, make_response,redirect
import mysql.connector
from datetime import timedelta, datetime
import os
from pyzbar import pyzbar
from PIL import Image
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import jwt as pyjwt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'snsdforever9'
app.config['MYSQL_DB'] = 'borrowingsystem'


app.config['JWT_SECRET_KEY'] = '963b5afdccdafbd06d384dca'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)


app.secret_key = '0094b98a02900a1254625937'

mydb = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect('/menu')
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        mycursor = mydb.cursor()
        query = "SELECT * FROM member WHERE username = %s"
        mycursor.execute(query, (id,))
        user = mycursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            login_user(User(id))
            payload = {
                'username': id                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
            }
            
            access_token = pyjwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

            session['access_token'] = access_token
            print(access_token)
            response = make_response(render_template('index.html',id=id))
            response.set_cookie('access_token', access_token)
            print(response)
            return response
        else:
            return render_template('login.html', message="Incorrect Username or Password")
    else:
        return render_template('login.html')

@app.route('/protected')
@login_required
def protected():
    return "Protected route: Only accessible by authenticated users"


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    response = make_response(redirect('/'))
    response.delete_cookie('access_token')
    print(response)
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        error_messages1 = []
        error_messages2 = []

        # Check if the username already exists
        mycursor = mydb.cursor()
        query = "SELECT username FROM member WHERE username = %s"
        mycursor.execute(query, (id,))
        existing_user = mycursor.fetchone()

        
        if not id.isdigit() or len(id) != 6:
            error_messages1.append("ID must be a 6-digit number.")
        if len(password) != 6:
            error_messages2.append("Password must be 6 characters.")
        if existing_user:
            error_messages1.append("Username already exists. Please choose a different username.")

        if len(error_messages1)>0 or len(error_messages2)>0:
            return render_template('register.html', error_messages1=error_messages1,error_messages2=error_messages2)
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query = "INSERT INTO member (username, password_hash) VALUES (%s, %s)"
            mycursor.execute(query, (id, hashed_password))
            mydb.commit()
            
            return render_template('login.html')
    
    return render_template('register.html')



@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    id = current_user.get_id()
    print(id)
    return render_template('index.html', id=id)




@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    id = current_user.get_id()
    return render_template('borrow.html', id=id)


@app.route('/return', methods=['GET', 'POST'])
@login_required
def Return():
    id = current_user.get_id()
    return render_template('return.html', id=id)

@app.route('/successborrow', methods=['POST'])
@login_required
def scan_qr_code():
    id = current_user.get_id()
    string_data = None
    check = True
    
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        tel = request.form['tel']
        day = request.form['day']
        ref = request.form['ref']

        error_messages = []
        decoded_data=""
        string_data = request.form['scanqr']
        print(string_data)

        mycursor=mydb.cursor()
        now = datetime.now()
        if len(id) != 6:
            error_messages.append("ID must be 6 numbers")
        if len(name) < 2:
            error_messages.append("Name must be at least 2 characters")
        if len(tel) != 10:
            error_messages.append("Your number must be 10 digits")

        if string_data == "":
            try :
                print("suay")
            # Get the uploaded file from the form
                qr_code = request.files['qr_code']
                # Open the uploaded file
                image = Image.open(qr_code)

                # Convert the image to grayscale
                grayscale_image = image.convert('L')
                # Decode the QR code
                decoded_data = pyzbar.decode(grayscale_image)
                
                string_data = decoded_data[0].data.decode('utf-8')
                print(string_data)
                if len(string_data) != 23:
                    check=False 
                    error_messages.append("Please input QR Code")
            except:
                decoded_data = []
                error_messages.append("Please input QR Code")
        elif len(string_data)!=23:
            error_messages.append("Wrong QR Code")
        
        try:
            day = int(day)
            if day > 0:
                print("valid")# Valid input, continue with the rest of the code
            else:
                error_messages.append("Number must be greater than 0")
        except ValueError:
            error_messages.append("Invalid input, please enter a number")

        sql = "SELECT name FROM staff WHERE id=%s"
        mycursor.execute(sql,(ref,))
        myresult = mycursor.fetchall()
        num =  len(myresult)
        if num==0:
            checkref = "None"
        else:   
            checkref = "in"

        if len(ref) != 6:
            error_messages.append("Your Reference ID must be 6 digits")
        elif checkref == "None":
            error_messages.append("No matching refference ID")
        

        
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
        print("=")
        print(string_data)

       
        
        owner_sql = "SELECT avaliable FROM user WHERE nstda_code=%s"
        mycursor.execute(owner_sql,(string_data,))
        myresult = mycursor.fetchall()
        num =  len(myresult)
        if num==0:
            avaliable = "None"
        else:   
            avaliable = myresult
            print(avaliable)

        
        #เช็คว่าชื่อยืมคืน
        namesql="SELECT name from data WHERE qr=%s"
        mycursor.execute(namesql,(string_data,))
        myresult = mycursor.fetchall()
        name_user=myresult

        sql = "SELECT name from staff WHERE id=%s"
        mycursor.execute(sql, (ref,))
        myresult = mycursor.fetchall()
        ref_id = myresult

        #เช้คลำดับ
        sql = "SELECT id FROM data"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        num = len(myresult)
        sequence = num+1
        print("ming")
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
                    sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status,ref,checkout,day,refname) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
                    values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,"borrow",ref,checkoutdate,day,ref_id[0][0])
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
                    sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status,ref,checkout,day,refname) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
                    values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,"borrow",ref,checkoutdate,day,ref_id[0][0])
                    mycursor.execute(sql, values)
                    mydb.commit()
                else:
                    error_messages.append("Not avaliable")
            
        if len(error_messages) > 0:
            for error in error_messages:
                flash(error)
            return render_template('borrow.html', messages=error_messages,id=id)
        
        return render_template('successborrow.html',newstuff=Stuff,newstrdata=string_data,newcheck = check,checkoutdate=checkoutdate,id=id)



@app.route('/successreturn', methods=['GET', 'POST'])
@login_required
def successreturn():
    id = current_user.get_id()
    string_data = None
    error_messages = []
    Stuff = None  
    check = False 

    if request.method == 'POST':
        id = request.form['id']
        ref = request.form['ref']
        mycursor = mydb.cursor()
        now = datetime.now()

        string_data = request.form['scanqr']
        print(string_data)

        if string_data == "":
            try :
                print("suay")
            # Get the uploaded file from the form
                qr_code = request.files['qr_code']
                # Open the uploaded file
                image = Image.open(qr_code)

                # Convert the image to grayscale
                grayscale_image = image.convert('L')
                # Decode the QR code
                decoded_data = pyzbar.decode(grayscale_image)
                
                string_data = decoded_data[0].data.decode('utf-8')
                print(string_data)
                if len(string_data) != 23:
                    check=False 
                    error_messages.append("Please input QR Code")
            except:
                decoded_data = []
                error_messages.append("Please input QR Code")
        elif len(string_data)!=23:
            error_messages.append("Wrong QR Code")

        sql = "SELECT name FROM staff WHERE id=%s"
        mycursor.execute(sql,(ref,))
        myresult = mycursor.fetchall()
        num =  len(myresult)
        if num==0:
            checkref = "None"
        else:   
            checkref = "in"

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

        sql = "SELECT name from staff WHERE id=%s"
        mycursor.execute(sql, (ref,))
        myresult = mycursor.fetchall()
        ref_id = myresult
        if myresult:
            ref_id = myresult[0][0]
        else:
            ref_id = None
        
        
        if len(id) != 6:
            error_messages.append("ID must be 6 numbers")
        elif checkref == "None":
            error_messages.append("No matching refference ID")

        if avaliable != "None":
            if ref_id != None:
                num = len(name_user)
                if avaliable[0][0] == "False":
                    
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

                            print(id)

                            insert_sql = """INSERT INTO data (sequence, id, name, stuff, tel, date, qr, owner, status, ref,refname)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
                            values = (sequence, id, name, stuff, tel, now.strftime(
                                '%Y-%m-%d %H:%M:%S'), string_data, Owner, "return", ref,ref_id)
                            sql = "UPDATE user SET avaliable = 'True' WHERE nstda_code = %s"
                            

                            session['insert_sql'] = insert_sql
                            session['values'] = values
                            session['sql'] = sql
                            session['string_data'] = string_data


                            now = datetime.now()
                            now_str = now.strftime('%Y-%m-%d')

                            if day is not None:
                                try:
                                    day_int = int(day)
                                    future_date = (
                                        now + timedelta(days=day_int)).strftime('%Y-%m-%d')
                                    print(now_str)
                                    print(future_date)

                                    if stuff != None:
                                        if future_date < now_str:
                                            warn = name+" Late Return"
                                            alertt = "Hi! "+name+" Do you want to return"+stuff+"?"
                                            return render_template('successreturn.html', warn=warn, newstuff=Stuff, newstrdata=string_data,
                                                                newcheck=check, alertt=alertt,)  # insert_sql=insert_sql, sql=sql, string_data=string_data, values=values)
                                        else:
                                            alertt = "Hi! "+name+" Do you want to return"+stuff+"?"
                                            print(insert_sql)
                                            print( values)
                                            print(sql)
                                            print( string_data)
                                            return render_template('successreturn.html', alertt=alertt, newstuff=Stuff, newstrdata=string_data,
                                                                newcheck=check,)  # insert_sql=insert_sql, sql=sql, string_data=string_data, values=values)

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
            return render_template('return.html', messages=error_messages,id=id)

    return render_template('successreturn.html',id=id)


@app.route('/confirm', methods=['GET'])
@login_required
def confirm():
    mycursor = mydb.cursor()
    insert_sql = session.get('insert_sql')
    values = session.get('values')
    sql = session.get('sql')
    string_data = session.get('string_data')

    if insert_sql and values:
        mycursor.execute(insert_sql, values)
        mydb.commit()
    if sql and string_data:
        mycursor.execute(sql, (string_data,))
        mydb.commit()
    return jsonify({'message': 'Data has been submitted'})

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    id = current_user.get_id()
    return render_template('history.html',id=id)


@app.route('/userrecord', methods=['GET', 'POST'])
@login_required
def userrecord():
    id = current_user.get_id()
    return render_template('userrecord.html',id=id)


@app.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    id = current_user.get_id()
    return render_template('overview.html',id=id)


@app.route('/accessinformation', methods=['GET', 'POST'])
@login_required
def accessinformation():
    id = current_user.get_id()
    return render_template('accessinformation.html',id=id)


@app.route('/notreturnstuff', methods=['GET', 'POST'])
@login_required
def notreturnstuff():
    id = current_user.get_id()
    return render_template('notreturnstuff.html',id=id)


@app.route('/checkdate', methods=['GET', 'POST'])
@login_required
def checkdate():
    id = current_user.get_id()
    return render_template('checkdate.html',id=id)


@app.route('/chart', methods=['GET', 'POST'])
@login_required
def chartperyear():
    id = current_user.get_id()
    return render_template('chart.html',id=id)


# findall users record
@app.route('/allborrow', methods=['GET', 'POST'])
@login_required
def alldataborrow():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )

    mycursor = mydb.cursor()
    sql = "SELECT * FROM data ORDER BY date DESC"
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
            "status": x[8]
        }
        data_list.append(data)
        print(data_list)

    return jsonify(data_list)

# borrowing information


@app.route('/borrowdata', methods=['POST'])
@login_required
def borrowdata():
    allData = request.json
    date = allData['date']
    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE status = 'borrow' AND  DATE(date) = '" +date+"' ORDER BY date DESC"
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


# return information
@app.route('/returndata', methods=['POST'])
@login_required
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
    sql = "SELECT * FROM data WHERE status = 'return' AND  DATE(date) = '" +date+"' ORDER BY date DESC"
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


@app.route('/notreturn', methods=['POST','GET'])
@login_required
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
            from datetime import datetime

            currentTime = datetime.now()
            other_date = datetime.strptime(x[10].strip(), "%Y-%m-%d")

            print(currentTime)
            print(type(currentTime))
            print(other_date)
            print(type(other_date))

            if other_date < currentTime:
                Check = False
                dayleft_str = "expired"
            else:
                Check = True
                dayleft = other_date - currentTime
                dayleft_str = str((dayleft.days)+1) + " days left"
                print(dayleft_str)

            for i in range(10):
                print(type(x[i]))
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
                "dayleft": dayleft_str,
                "check": Check,
            }
            data_list.append(data)
    data_list = sorted(data_list, key=lambda x: x['day'], reverse=False)

    return jsonify(data_list)


@app.route('/qrdata', methods=['POST'])
@login_required
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
    sql = "SELECT * FROM data WHERE qr = '"+qr+"' ORDER BY date DESC "
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
@login_required
def returnyear():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="snsdforever9",
        database="borrowingsystem"
    )
    allData = request.json
    year = allData['year']
    option = allData['option']
    mycursor = mydb.cursor()

    if option == "return":
        sql = "SELECT * FROM data WHERE YEAR(date) LIKE %s AND status = 'return' ORDER BY date DESC"
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
        sql = "SELECT * FROM data WHERE YEAR(date) LIKE %s AND status = 'borrow' ORDER BY date DESC"
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
@login_required
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

    if option == "return":
        sql = "SELECT * FROM data WHERE YEAR(date) LIKE %s AND MONTH(date) LIKE %s AND status = 'return' ORDER BY date DESC "
        mycursor.execute(sql, (year, month,))
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
        sql = "SELECT * FROM data WHERE YEAR(date) = %s AND MONTH(date) = %s AND status = 'borrow' ORDER BY date DESC"
        mycursor.execute(sql, (year, month,))
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
@login_required
def chartborrow():
    mycursor = mydb.cursor()
    data_list = []
    allData = request.json
    year = allData['year']
    for month in range(1, 13):
        sql = "SELECT COUNT(*) AS times FROM data WHERE YEAR(date) = %s AND MONTH(date) = %s AND status = 'borrow'"
        mycursor.execute(sql, (year, month,))
        result = mycursor.fetchone()
        times = result[0]

        data = {
            "month": month,
            "times": times
        }
        data_list.append(data)

    return jsonify(data_list)


@app.route('/chartreturn', methods=['POST'])
@login_required
def chartreturn():

    allData = request.json
    year = allData['year']

    mycursor = mydb.cursor()
    data_list = []

    for month in range(1, 13):
        sql = "SELECT COUNT(*) AS times FROM data WHERE YEAR(date) = %s AND MONTH(date) = %s AND status = 'return'"
        mycursor.execute(sql, (year, month,))
        result = mycursor.fetchone()
        times = result[0]

        data = {
            "month": month,
            "times": times
        }
        data_list.append(data)

    return jsonify(data_list)


@app.route('/accessinfor', methods=['GET', 'POST'])
@login_required
def accessinfor():
    id = current_user.get_id()
    string_data = request.form['scanqr']
    if request.method == 'POST':
        print(string_data)
        print(len(string_data))
        error_messages = []
        error=[]
        decoded_data = []
        if string_data == "":
            try :
                # Get the uploaded file from the form
                qr_code = request.files['qr_code']
                # Open the uploaded file
                image = Image.open(qr_code)

                # Convert the image to grayscale
                grayscale_image = image.convert('L')
                # Decode the QR code
                decoded_data = pyzbar.decode(grayscale_image)
                
                string_data = decoded_data[0].data.decode('utf-8')
                
                if len(string_data) != 23:
                    check=False 
                    error.append("Wrong QR Code")
            except:
                decoded_data = []
                error.append("Please input QR Code")
                error_messages.append("No data found")
        elif len(string_data)!=23:
            error.append("Wrong QR Code")
        elif len(string_data)==23:
            sql = "SELECT nstda_code from user WHERE nstda_code=%s"
            mycursor = mydb.cursor()
            mycursor.execute(sql, (string_data,))
            myresult = mycursor.fetchall()
            if not myresult:
                error.append("Wrong QR Code")
 
        print(decoded_data)
        if string_data:
            mycursor = mydb.cursor()

            sql = "SELECT * from data WHERE qr=%s"
            mycursor.execute(sql, (string_data,))
            myresult = mycursor.fetchall()
            print(myresult)

            nsql = "SELECT first_name from user WHERE nstda_code=%s"
            mycursor.execute(nsql, (string_data,))
            ownresult = mycursor.fetchall()
            namestuff = "Stuff: " + str(ownresult[0][0]) if ownresult else ""

            osql = "SELECT last_name from user WHERE nstda_code=%s"
            mycursor.execute(osql, (string_data,))
            stuffresult = mycursor.fetchall()
            nameowner = "Owner: " + str(stuffresult[0][0]) if stuffresult else ""
            print(nameowner)

            if myresult == []:
                error_messages.append("No data found")

            data_list = []
            num = len(myresult)+1
            print(num)
            for index, x in enumerate(myresult, start=num):
                num = num -1
                data = {
                    "order": num,
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
                data_list = sorted(data_list, key=lambda x: x['date'], reverse=True)

            if error_messages:
                return render_template('accessinformation.html', stuff=namestuff, owner=nameowner,messages=error_messages,messages2=error,id=id)
            else:
                return render_template('accessinformation.html', data_list=data_list, stuff=namestuff, owner=nameowner,messages2=error,id=id)

    return render_template('accessinformation.html', messages=error_messages,messages2=error,id=id)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', "0.0.0.0"),
            port=int(os.getenv('PORT', 4444)))