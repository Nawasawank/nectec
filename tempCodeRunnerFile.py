@app.route('/access', methods=['GET', 'POST'])
def access():
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

    