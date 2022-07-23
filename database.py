import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",  # add your password
  database = "hemodialysis"
)

mycursor = mydb.cursor()


# mycursor.execute("CREATE TABLE user (id INT(8) AUTO_INCREMENT, Name VARCHAR(50), passw VARCHAR(12), role VARCHAR(8), flag VARCHAR(8), gender VARCHAR(20), BDate date, email VARCHAR(320), ssn VARCHAR(50), phonenumber VARCHAR(50), lastname VARCHAR (255), PRIMARY KEY (id))")
# mycursor.execute("CREATE TABLE doctor (id INT(8), name VARCHAR(255), schedule time, email VARCHAR(50). PRIMARY KEY (id))")
# mycursor.execute("CREATE TABLE patient (id INT(8), name VARCHAR(50), dr_ID INT(8), reservation date, time time, doctor_comment VARCHAR(255), history VARCHAR(255), gender VARCHAR(8), photo VARCHAR(255), BDate date, email VARCHAR(320), phonenumber VARCHAR(50), lastname VARCHAR(255), ssn VARCHAR(50) , PRIMARY KEY (id))")
# mycursor.execute("CREATE TABLE appointments (app_ID INT(8) AUTO_INCREMENT, patient_ID INT(8), reservation date, time time, count INT(8), PRIMARY KEY(app_ID), FOREIGN KEY (patient_ID) REFERENCES patient(ID))")
# mycursor.execute("CREATE TABLE DrTime (APPID INT(8) AUTO_INCREMENT, DrID INT(8), PatientID INT(8), DATE date, time time, PRIMARY KEY(APPID), FOREIGN KEY (patientID) REFERENCES patient(id),FOREIGN KEY (DrID) REFERENCES doctor(id))")
# mycursor.execute("CREATE TABLE DrTimeWTP (APPID INT(8) AUTO_INCREMENT, DrID INT(8), time time, PRIMARY KEY(APPID),FOREIGN KEY (DrID) REFERENCES doctor(id))")       
# mycursor.execute("CREATE TABLE SCANS (scan_id INT(8) AUTO_INCREMENT, pat_id INT, photo_path VARCHAR(255), dr_id INT(8), PRIMARY KEY (scan_id), FOREIGN KEY (pat_id) REFERENCES patient(id))")
# mycursor.execute("CREATE TABLE inventory (deviceID INT(8) AUTO_INCREMENT, room_num INT(8), DrID INT(8), installation date, last_service date, upcoming_service date, catalog_ref_id VARCHAR(40), PRIMARY KEY(deviceID), FOREIGN KEY (DrID) REFERENCES doctor(id))")


# # query="ALTER TABLE appointments ALTER count SET DEFAULT 1"
# # mycursor.execute(query)
# # mydb.commit()




