from flask import Flask, render_template,request,flash,redirect,url_for,session
import mysql.connector
import datetime
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



@app.route('/success', methods=['POST'])
def scan_qr_code():
    # Get the uploaded file from the form
    qr_code = request.files['qr_code']

    # Open the uploaded file
    image = Image.open(qr_code)

    # Convert the image to grayscale
    grayscale_image = image.convert('L')

    # Decode the QR code
    decoded_data = pyzbar.decode(grayscale_image)
    print(decoded_data)

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
        mycursor=mydb.cursor()
        now = datetime.datetime.now()
        option = request.form['option']
        error_messages = []

        if len(id) != 13:
            error_messages.append("ID must be 13 characters")
        if len(name) < 2:
            error_messages.append("Name must be at least 2 characters")
        if len(tel) != 10:
            error_messages.append("Your number must be 10 digits")

        
        #เชื่อมเจ้าของ
        owner_sql = "SELECT nstda_code FROM user"
        mycursor.execute(owner_sql)
        owner_myresult = mycursor.fetchall()

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
        #print(string_data)
        #print(myresult[0])
        #print(type(check))


        #อัพเดทสถานะด้วยการเช้ครหัส
        sql = "SELECT nstda_code FROM user"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        num = len(myresult)
        count = 0
        for i in range(num):
            if string_data==myresult[i][0]:
                count = i
        ##print(myresult)
        print(count)
        print(string_data)

        owner_sql = "SELECT avaliable FROM user WHERE nstda_code=%s"
        mycursor.execute(owner_sql,(string_data,))
        myresult = mycursor.fetchall()
        avaliable = myresult


        '''if option == "borrow":
            sql = "UPDATE user SET avaliable = 'False' WHERE nstda_code = %s"
            mycursor.execute(sql,(string_data,))
            mydb.commit()

        if option == "return":
            sql = "UPDATE user SET avaliable = 'True' WHERE nstda_code = %s"
            mycursor.execute(sql,(string_data,))
            mydb.commit()'''
        
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

        #checkid
        namesql="SELECT id from data WHERE qr=%s"
        mycursor.execute(namesql,(string_data,))
        myresult = mycursor.fetchall()
        id_user=myresult

        #checktel
        namesql="SELECT tel from data WHERE qr=%s"
        mycursor.execute(namesql,(string_data,))
        myresult = mycursor.fetchall()
        tel_user=myresult

        #insert information
        if str(string_data)!="None":
            num=len(name_user)
            if option=="borrow":
                if avaliable[0][0] =="True":
                    nsql = "UPDATE user SET avaliable = 'False' WHERE nstda_code = %s"
                    mycursor.execute(nsql,(string_data,))
                    mydb.commit()
                    sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s)"
                    values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,option)
                    mycursor.execute(sql, values)
                    mydb.commit()
                elif num==0:
                    nsql = "UPDATE user SET avaliable = 'False' WHERE nstda_code = %s"
                    mycursor.execute(nsql,(string_data,))
                    mydb.commit()
                    
                    sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s)"
                    values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,option)
                    mycursor.execute(sql, values)
                    mydb.commit()
                else:
                    error_messages.append("Not avaliable")
            elif option=="return":
                if avaliable[0][0] =="False":
                    if not name_user[-1][0] == name:
                        error_messages.append("incorrect name")
                    if not id_user[-1][0]==id:
                        error_messages.append("incorrect id")
                    if not tel_user[-1][0]==tel:
                        error_messages.append("incorrect number")
                    if id_user[-1][0]==id:
                        if name_user[-1][0] == name:
                            if tel_user[-1][0]==tel:
                                sql = "INSERT INTO data (sequence,id, name,stuff, tel,date,qr,owner,status) VALUES (%s,%s, %s, %s, %s,%s, %s,%s,%s)"
                                values = (sequence,id, name, Stuff,tel,now.strftime('%Y-%m-%d %H:%M:%S'),string_data,Owner,option)
                                mycursor.execute(sql, values)
                                mydb.commit()

                                sql = "UPDATE user SET avaliable = 'True' WHERE nstda_code = %s"
                                mycursor.execute(sql,(string_data,))
                                mydb.commit()
                else:
                    error_messages.append("have nothing to return")
        
        if len(error_messages) > 0:
            for error in error_messages:
                flash(error)
            return redirect(url_for('index'))
        
        return render_template('success.html',newstuff=Stuff,newoption=option,newstrdata=string_data,newcheck = check)

if __name__ == "__main__":
    app.run("0.0.0.0",5000)