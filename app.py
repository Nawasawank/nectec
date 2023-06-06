from flask import Flask, render_template,request
import mysql.connector
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'snsdforever9'
app.config['MYSQL_DB'] = 'borrowing_system'

mydb = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

ownerdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="snsdforever9",
    database="db_unai" )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def successs():
    return render_template('success.html')

@app.route('/success', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        tel = request.form['tel']
        stuff = request.form['stuff']
        mycursor=mydb.cursor()
        now = datetime.datetime.now()
        sql = "INSERT INTO data (id, name, tel, stuff,date) VALUES (%s, %s, %s, %s, %s)"
        values = (id, name, tel, stuff,now.strftime('%Y-%m-%d %H:%M:%S'))
        mycursor.execute(sql, values)
        mydb.commit()

        '''if stuff != "": 
            mycursor=ownerdb.cursor() 
            sql = "SELECT first_name FROM user"
            mycursor.execute(sql)
            mythings = mycursor.fetchall()
            for things in mythings:
                if things==stuff:
                    sql = "SELECT last_name FROM data WHERE last_name = %s"
                    mycursor.execute(sql,(stuff))
                    myowner = mycursor.fetchall()
                    for owner in myowner:
                        sql = "INSERT INTO data (owner) VALUES (%s)"
                        values = (owner)
                        mycursor.execute(sql, values)
                        mydb.commit()'''



        return f"Form Submitted Successfully!"
    

if __name__ == "__main__":
    app.run("0.0.0.0",5000)