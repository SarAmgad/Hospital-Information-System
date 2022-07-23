from dataclasses import is_dataclass
from unittest import result
import mysql.connector
from email import message
from flask import Flask, redirect, render_template, request, session, url_for, flash
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.secret_key = 'secret key'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex1 = r'^(?:\+?44)?[07]\d{9,13}$'


def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


def phonenumber(num):
    if(re.fullmatch(regex1, num)):
        return True
    else:
        return False


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="sara2001",
    database="hemodialysis"
)

mycursor = mydb.cursor(buffered=True)


@app.route('/')
def index():
    session.clear()
    return render_template("index.html")


@app.route('/aboutus')
def aboutus():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/doctors', methods=["GET", "POST"])
def doctors():
    sql = '''SELECT * from doctor INNER JOIN drtimewtp ON doctor.id = drtimewtp.DrID'''
    sql = "SELECT * FROM doctor "
    mycursor.execute(sql) 
    result = mycursor.fetchall()

    return render_template('doctors.html', data = result)


@app.route('/reservationnn', methods=["GET", "POST"])
def reservationnn():
    print("hi")
    mycursor.execute("SELECT DrID FROM drtimewtp")
    result = mycursor.fetchall()
    if request.form == "POST":
        id = request.form['id']
        date = request.form['date']
        print(id)
        print("bye")
        print(date)
        mycursor.execute(
        'INSERT INTO drtime (DrID, PatientID,date) VALUES( %s, %s, %s,%s)', (id, patientID[0],date))
        mydb.commit()
    return render_template('doctors.html', result = result)


@app.route('/blog')
def blog():
    return render_template("blog.html")


@app.route('/login&reg')
def log_reg():
    return render_template("signup.html")


@app.route('/log')
def log():
    return render_template("signin.html")


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/devices')
def devices():
    mycursor.execute("SELECT * FROM inventory")
    myresult2 = mycursor.fetchall()
    return render_template('devices.html', Data=myresult2)


@app.route('/doctor')
def doctor():
    return render_template("doctor.html")


@app.route('/patient')
def patient():
    return render_template("patient.html")


@app.route('/aftersignup')
def aftersignup():
    return render_template("aftersignup.html")


@app.route('/appointments')
def appointments():
    mycursor.execute("SELECT * FROM appointments")
    myresult4 = mycursor.fetchall()
    return render_template('appointments.html',  INFO=myresult4)


@app.route('/patients')
def patients():
    mycursor.execute("SELECT * FROM patient")
    myresult2 = mycursor.fetchall()
    return render_template('patients.html', Data=myresult2)


@app.route('/doctorpatients')
def doctorpatients():
    mycursor.execute("SELECT * FROM patient WHERE dr_ID = %s", DoctorID)
    result = mycursor.fetchall()
    return render_template('doctorpatients.html', Data=result)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['id']
        if (check_email(username) == False):
            error_statment = 'Enter a valid Email.'
            return render_template("signin.html", error_statement=error_statment)

        elif len(password) == 0 or len(username) == 0:
            error_statement = 'Wrong Password or Email.'
            return render_template("signin.html", error_stat=error_statement)

        else:
            mycursor.execute(
                'SELECT flag FROM user WHERE passw =%s', (password,))
            flag = mycursor.fetchone()
            if flag == ("false",):
                msg = "You Can't Login, Call Admin for Response."
                return render_template('signin.html', error=msg)
            else:
                mycursor.execute(
                    'SELECT * FROM user WHERE email = %s AND passw = %s ', (username, password,))
                account = mycursor.fetchall()
                if account:
                    mycursor.execute(
                        'SELECT role from user WHERE email=%s AND passw =%s', (username, password,))
                    roles = mycursor.fetchone()
                    if roles == ("patient",):
                        session['user_p'] = username
                        mycursor.execute(
                            'SELECT Name from user WHERE email=%s AND passw =%s', (username, password,))
                        pname = mycursor.fetchone()[0]

                        mycursor.execute(
                            'SELECT id from user WHERE email=%s AND passw =%s', (username, password,))
                        global patientID
                        patientID = mycursor.fetchone()
                        return render_template("patient.html", name='Welcome {}'.format(pname))
                    elif roles == ("doctor",):
                        session['user_d'] = username
                        mycursor.execute(
                            'SELECT Name from user WHERE email=%s AND passw =%s', (username, password,))
                        dname = mycursor.fetchone()[0]
                        mycursor.execute(
                            'SELECT id from user WHERE email=%s AND passw =%s', (username, password,))
                        global DoctorID
                        DoctorID = mycursor.fetchone()

                        return render_template('doctor.html', name='Welcome {}'.format(dname))
                    else:
                        session['user_a'] = username
                        mycursor.execute(
                            'SELECT Name from user WHERE email=%s AND passw =%s', (username, password,))
                        aname = mycursor.fetchone()[0]
                        mycursor.execute(
                            'SELECT id from user WHERE email=%s AND passw =%s', (username, password,))
                        return render_template('admin.html', name='Welcome {}'.format(aname))
                else:
                    msg = " You don't have an account."
                    return render_template('signin.html', error=msg)


@app.route('/SignUp', methods=["Get", "POST"])
def SignUp():
    if request.method == 'POST' and 'name' in request.form and 'id' in request.form:
        user = request.form['email']
        passw = request.form['id']
        role = request.form['role']
        fname = request.form['name']
        lname = request.form['lastname']
        bd = request.form['date']
        num = request.form['phonenumber']
        ssn = request.form['ssn']
        gender = request.form['gender']
        isInt1 = True
        isInt2 = True
        try:
            int(fname)
        except ValueError:
            isInt1 = False

        try:
            int(lname)
        except ValueError:
            isInt2 = False

        

        if isInt1 and isInt2 and len(passw) < 8 and (phonenumber(num) == False) and (check_email(user) == False):
            error_statment1 = 'You should enter a text not numbers.'
            error_statement2 = 'Password must be 8 characters.'
            error_statement3 = 'Enter a valid Email'
            error_statement4 = 'Enter a valid phone number'
            return render_template('signup.html', error_statm1=error_statment1, error_statm2=error_statment1, error_statm3=error_statement2,
                                   error_statm4=error_statement3, error_statm5=error_statement4,
                                   name=fname, lastname=lname, email=user, passwd=passw, ssn=ssn)
        
        
        elif isInt1:
            error_statment = 'You should enter a text not numbers.'
            return render_template("signup.html", error_statm1=error_statment,
                                   name=fname, lastname=lname, email=user, passwd=passw, ssn=ssn)

        elif isInt2:
            error_statment = 'You should enter a text not numbers.'
            return render_template("signup.html", error_statm2=error_statment,
                                   name=fname, lastname=lname, email=user, passwd=passw, ssn=ssn)

        elif len(passw) < 8:
            error_statment = 'Password must be 8 characters.'
            return render_template('signup.html', error_statm3=error_statment, name=fname, lastname=lname, email=user,
                                   passwd=passw, ssn=ssn)

        elif (check_email(user) == False):
            error_statment = 'Enter a valid Email'
            return render_template('signup.html', error_statm3=error_statment, name=fname, lastname=lname, email=user,
                                   passwd=passw, ssn=ssn)

        elif (phonenumber(num) == False):
            error_statment = 'Enter a valid phone number'
            return render_template("signup.html", error_statm5=error_statment,
                                   name=fname, lastname=lname, email=user, passwd=passw, ssn=ssn)

        else:
            error_statment = ''

        if error_statment == '':
            mycursor.execute(
                'SELECT * FROM user WHERE email =%s  ', ( user,))
            account = mycursor.fetchall()
            mycursor.execute(
                'SELECT * FROM user WHERE ssn =%s  ', ( ssn,))
            account1 = mycursor.fetchall()
            mycursor.execute(
                'SELECT * FROM user WHERE phonenumber =%s  ', ( num,))
            account2 = mycursor.fetchall()

            if account:
                error_statment = "This email is already taken."
            elif account1:
                error_statment = "The SSN is already taken."
            elif account2:
                error_statment = "The phone number is already taken."

            else:
                if role == "patient":
                    s= "true"
                    mycursor.execute(
                        'INSERT INTO user (passw,email,role, Name, lastname, gender, phonenumber, ssn,BDate,flag) VALUES( %s, %s,%s, %s, %s,%s, %s,%s,%s,%s)', (passw, user, role, fname, lname, gender, num, ssn,bd,s))
                    mydb.commit()
                    mycursor.execute(
                        'SELECT id from user WHERE email=%s AND passw =%s', (user, passw,))
                    result = mycursor.fetchone()
                    mycursor.execute(
                        'INSERT INTO patient (id, email, Name, lastname, gender, phonenumber, ssn,BDate) VALUES( %s, %s, %s,%s, %s,%s,%s,%s)', (result[0], user, fname, lname, gender, num, ssn,bd))
                    mydb.commit()

                else:
                    s = "false"
                    mycursor.execute(
                        'INSERT INTO user (passw,email,role, Name, lastname, gender, phonenumber, ssn,flag,BDate) VALUES( %s, %s,%s, %s, %s,%s, %s,%s,%s,%s)', (passw, user, role, fname, lname, gender, num, ssn, s,bd))
                    mydb.commit()

        if error_statment == '':
            if role == "patient":
                return render_template('aftersignup.html', Log='Log in')
            else:
                return render_template('aftersignup.html', msg='Wait for acceptance.', home='Back to Homepage.')
        else:
            return render_template("signup.html", error=error_statment,
                                   name=fname, lastname=lname, email=user, passwd=passw, ssn=ssn)


# the page where new doctors requests appear
@app.route('/Edit')
def editTable():
    mycursor.execute('SELECT id,name,passw,flag FROM user WHERE flag ="false"')
    user = mycursor.fetchall()
    return render_template('dashboard.html', user=user)


# decline a dr signup
@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    mycursor.execute("DELETE FROM user WHERE id=%s", (id_data,))
    mydb.commit()
    flash("Record Has Been Deleted Successfully.")
    return redirect(url_for('editTable'))


# accept a doctor signup
@app.route('/update/<string:id_data>', methods=['GET', 'POST'])
def update(id_data):
    mycursor.execute(" UPDATE user SET flag=%s WHERE id=%s", ("true", id_data))
    mydb.commit()
    mycursor.execute('SELECT * from user WHERE id = %s', (id_data,))
    result = mycursor.fetchone()
    mycursor.execute(
        'INSERT INTO doctor (id,name,email) VALUES( %s, %s, %s)', (result[0], result[1], result[7],))
    mydb.commit()
    flash("Data Updated Successfully.")
    return redirect(url_for('editTable'))


# deleting doctors in admin
@app.route('/Delete', methods=["POST"])
def Delete():
    if request.method == 'POST' and 'id3' in request.form:
        Id = request.form['id3']
        mycursor.execute("DELETE FROM doctor WHERE id = %s", (Id,))
        mydb.commit()
        flash('deleted sucesfully')
    return redirect(url_for('doctors'))


@app.route('/add_comment', methods=['Get', 'POST'])
def add_comment():
    if request.method == 'POST':
        num = request.form['id']
        comment = request.form['comment']
        mycursor.execute(
            "UPDATE patient SET doctor_comment= %s WHERE ID=%s ", (comment, num))
        mydb.commit()
    return redirect(url_for('doctorpatients'))


@app.route('/reserve', methods=['Get', 'POST'])
def reserve():
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        time = request.form['time']

        mycursor.execute(
            "SELECT count FROM appointments WHERE reservation = %s AND time = %s", (date, time))
        counter = mycursor.fetchone()

        print(counter)
        if counter == None:
            print("hii")
            mycursor.execute(
                " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (id, date, time))
            mycursor.execute(
                "UPDATE patient SET reservation= %s WHERE id=%s ", (date, id))
            mycursor.execute(
                "UPDATE patient SET time= %s WHERE id=%s ", (time, id))
            mydb.commit()

        elif counter == (1,):
            mycursor.execute(
                " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (id, date, time))
            mycursor.execute(
                "UPDATE patient SET reservation= %s WHERE id=%s ", (date, id))
            mycursor.execute(
                "UPDATE patient SET time= %s WHERE id=%s ", (time, id))
            mycursor.execute(
                "UPDATE appointments SET count= %s WHERE reservation = %s AND time = %s ", (2, date, time))
            mydb.commit()

        elif counter == (2,):
            mycursor.execute(
                " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (id, date, time))
            mycursor.execute(
                "UPDATE patient SET reservation= %s WHERE id=%s ", (date, id))
            mycursor.execute(
                "UPDATE patient SET time= %s WHERE id=%s ", (time, id))
            mycursor.execute(
                "UPDATE appointments SET count= %s WHERE reservation = %s AND time = %s ", (3, date, time))
            mydb.commit()

        elif counter == (3,):
            mycursor.execute(
                " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (id, date, time))
            mycursor.execute(
                "UPDATE patient SET reservation= %s WHERE id=%s ", (date, id))
            mycursor.execute(
                "UPDATE patient SET time= %s WHERE id=%s ", (time, id))
            mycursor.execute(
                "UPDATE appointments SET count= %s WHERE reservation = %s AND time = %s ", (4, date, time))
            mydb.commit()

        else:
            print("noo")
            print("hii")

    return redirect(url_for('patients'))


@app.route('/remove', methods=["POST"])
def remove():
    if request.method == 'POST' and 'id3' in request.form:
        Id = request.form['id3']
        mycursor.execute("DELETE FROM patient WHERE id = %s", (Id,))
        mycursor.execute("DELETE FROM user WHERE id = %s", (Id,))
        mycursor.execute(
            "DELETE FROM appointments WHERE patient_ID = %s", (Id,))
        mydb.commit()
        flash('deleted sucesfully')
    return redirect(url_for('patients'))


@app.route('/reserve_patient', methods=['Get', 'POST'])
def reserve_patient():
    if request.method == 'POST' and 'id6' in request.form and 'id7' in request.form:
        date = request.form['id6']
        time = request.form['id7']

        mycursor.execute(
            'SELECT * FROM appointments WHERE patient_ID =%s AND reservation =%s', (patientID[0], date))
        account = mycursor.fetchone()
        if account:
            msg = "You already have an appointment on this date."

        else:
            mycursor.execute(
                "SELECT count FROM appointments WHERE reservation = %s AND time = %s", (date, time))
            counter = mycursor.fetchone()

            print(counter)
            if counter == None:
                print("hii")
                mycursor.execute(
                    " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (patientID[0], date, time))
                mycursor.execute(
                    "UPDATE patient SET reservation= %s WHERE id=%s ", (date, patientID[0]))
                mycursor.execute(
                    "UPDATE patient SET time= %s WHERE id=%s ", (time, patientID[0]))
                mydb.commit()
                msg = ''

            elif counter == (1,):
                mycursor.execute(
                    " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (patientID[0], date, time))
                mycursor.execute(
                    "UPDATE patient SET reservation= %s WHERE id=%s ", (date, patientID[0]))
                mycursor.execute(
                    "UPDATE patient SET time= %s WHERE id=%s ", (time, patientID[0]))
                mycursor.execute(
                    "UPDATE appointments SET count= %s WHERE reservation = %s AND time = %s ", (2, date, time))
                mydb.commit()
                msg = ''

            elif counter == (2,):
                mycursor.execute(
                    " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (patientID[0], date, time))
                mycursor.execute(
                    "UPDATE patient SET reservation= %s WHERE id=%s ", (date, patientID[0]))
                mycursor.execute(
                    "UPDATE patient SET time= %s WHERE id=%s ", (time, patientID[0]))
                mycursor.execute(
                    "UPDATE appointments SET count= %s WHERE reservation = %s AND time = %s ", (3, date, time))
                mydb.commit()
                msg = ''

            elif counter == (3,):
                mycursor.execute(
                    " INSERT INTO appointments (patient_ID,reservation,time) VALUES( %s, %s,%s)", (patientID[0], date, time))
                mycursor.execute(
                    "UPDATE patient SET reservation= %s WHERE id=%s ", (date, patientID[0]))
                mycursor.execute(
                    "UPDATE patient SET time= %s WHERE id=%s ", (time, patientID[0]))
                mycursor.execute(
                    "UPDATE appointments SET count= %s WHERE reservation = %s AND time = %s ", (4, date, time))
                mydb.commit()
                msg = ''

            else:
                msg = "Sorry this time is fully booked."
    mycursor.execute(
        "SELECT * FROM appointments WHERE patient_ID = %s", patientID)
    result = mycursor.fetchall()

    return render_template("patientappointments.html", INFO=result, msg=msg)


@app.route('/delete_res/<string:id_data>', methods=['GET'])
def delete_res(id_data):
    mycursor.execute("DELETE FROM appointments WHERE app_id=%s", (id_data,))
    mydb.commit()
    mycursor.execute(
        "SELECT * FROM appointments WHERE patient_ID = %s", patientID)
    result = mycursor.fetchall()
    return render_template("patientappointments.html", INFO=result)


@app.route('/patientappointments')
def patientappointments():
    mycursor.execute(
        "SELECT * FROM appointments WHERE patient_ID = %s", patientID)
    result = mycursor.fetchall()

    return render_template('patientappointments.html',  INFO=result)


@app.route('/myhistory')
def myhistory():
    global patientID
    mycursor.execute("SELECT * FROM patient WHERE id = %s", patientID)
    result = mycursor.fetchone()
    name = result[1]
    p_id = result[0]
    history = result[6]
    gender = result[7]
    drcomment = result[5]
    if result[8] == None:
        image_file = url_for('static', filename='uploads/' + 'unknown.jpg')
    else:
        image_file = url_for('static', filename='uploads/' + result[8])
    if history == None:
        history = ' '
    if drcomment == None:
        drcomment='No new comment from the doctor.'

    mycursor.execute(
        "SELECT photo_path FROM scans WHERE pat_ID = %s", patientID)
    scan = mycursor.fetchall()
    for i in scan:
        print(i[0])
    return render_template("patienthistory.html", history=history, gender=gender, name=name, p_id=p_id, drcomment=drcomment, image=image_file, scan=scan)


@app.route('/deletedr/<string:id1_data>', methods=['GET'])
def deletedr(id1_data):
    mycursor.execute("DELETE FROM doctor WHERE id=%s", (id1_data,))
    mydb.commit()
    return redirect(url_for('doctors'))


@app.route('/doctor_reserve', methods=['Get', 'POST'])
def doctor_reserve():
    mycursor.execute("SELECT name, DATE, time FROM doctor INNER JOIN drtimewtp ON id = drID")
    myresult2 = mycursor.fetchall()
    return render_template('doctorreserve.html', Data=myresult2)


@app.route('/doctor_show', methods=['Get', 'POST'])
def show():
    mycursor.execute("SELECT time FROM drtimewtp")
    result = mycursor.fetchall()
    return render_template('doctors.html', result = result)



@app.route('/done',methods =['Get','POST']) 
def done():
   if request.method == 'POST' and 'fname' in request.form and 'dname' in request.form and 'tname' in request.form :
      name= request.form['fname']
      date = request.form['dname']
      hour = request.form['tname']
      mycursor.execute(" SELECT id FROM doctor WHERE name = %s ", (name))
      id = mycursor.fetchone()
      mycursor.execute(
                    "UPDATE patient SET dr_ID= %s WHERE id=%s ", (id, patientID[0],))
      mydb.commit()
   return redirect(url_for('doctorreserve')) 


@app.route('/upload_profilepicture', methods=['GET', 'POST'])
def upload_profilepicture():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('upload_image filename: ' + filename)
    mycursor.execute("UPDATE patient SET photo= %s WHERE id=%s ",
                     (filename, patientID[0]))
    mydb.commit()
    return redirect(url_for('myhistory'))


@app.route('/upload_scans', methods=['GET', 'POST'])
def upload_scans():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('upload_image filename: ' + filename)
    mycursor.execute(
        "SELECT dr_ID FROM patient WHERE id = %s", (patientID[0],))
    drid = mycursor.fetchone()
    mycursor.execute(
        "INSERT INTO scans (pat_id, photo_path,dr_id) VALUES( %s, %s,%s)", (patientID[0], filename, drid[0]))
    mydb.commit()
    return redirect(url_for('myhistory'))


@app.route('/viewscans', methods=['Get', 'POST'])
def viewscans():
    if request.method == 'POST':
        Id = request.form['id']
        mycursor.execute(
            "SELECT photo_path FROM scans WHERE pat_id = %s AND dr_id = %s", (Id, DoctorID[0]))
        scan = mycursor.fetchall()

    mycursor.execute("SELECT * FROM patient WHERE dr_ID = %s", DoctorID)
    result = mycursor.fetchall()
    return render_template('doctorpatients.html', Data=result, scan=scan)



@app.route('/upload_scansadmin', methods=['GET', 'POST'])
def upload_scansadmin():
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    name = request.form['admin']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print('upload_image filename: ' + filename)
    mycursor.execute(
        "SELECT dr_ID FROM patient WHERE id = %s", (name,))
    drid = mycursor.fetchone()
    mycursor.execute(
        "INSERT INTO scans (pat_id, photo_path,dr_id) VALUES( %s, %s,%s)", (name, filename, drid[0],))
    mydb.commit()
    mycursor.execute("SELECT * FROM patient")
    myresult2 = mycursor.fetchall()
    return render_template('patients.html', Data=myresult2)
    



@app.route('/reserve1', methods=['Get', 'POST'])
def reserve1():
    mycursor.execute("SELECT * FROM doctor")
    if request.method == 'POST':
        id = request.form['id']
        date = request.form['date']
        hour = request.form['time']
        mycursor.execute(" INSERT INTO drtime (DATE,time,drID,patientID) VALUES( %s, %s,%s,%s)",(date,hour,id,patientID[0]))
        mydb.commit()
        mycursor.execute("UPDATE patient SET dr_ID= %s WHERE id=%s ", (id, patientID[0],))

        mydb.commit()
    return redirect(url_for('doctors'))

@app.route('/doctorappointments')
def doctorappointments():
    mycursor.execute("SELECT * FROM drtime WHERE DrID = %s",(DoctorID[0],))
    myresult4 = mycursor.fetchall()
    return render_template('appointments.html',  data=myresult4)



if __name__ == '__main__':
    app.run(debug=True, port=3000)
