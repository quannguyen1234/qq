import pyrebase
import os



config = {
  'apiKey': "AIzaSyBa7gOp-OzeSLmshRoqvdXHJQVAxqmlmn4",
  'authDomain': "doctor-farmily.firebaseapp.com",
  'databaseURL': "https://doctor-farmily-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "doctor-farmily",
  'storageBucket': "doctor-farmily.appspot.com",
  'messagingSenderId': "831614639402",
  'appId': "1:831614639402:web:2b2c29e211082b91139253",
  'measurementId': "G-7EK6PDFTTL"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
fb_database=firebase.database()

# Create Authentication user account in firebase  
auth = firebase.auth()

# # Enter your user account details 
email = "nhquan0911@gmail.com"
password = "quan9112001"

firebase_admin = auth.sign_in_with_email_and_password(email, password)

