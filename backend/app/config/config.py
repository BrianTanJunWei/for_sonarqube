# Import flask and datetime module for showing date and time
from datetime import timedelta
import uuid  # Import the uuid module
from flask import Flask, request, jsonify , session
from flask_cors import CORS
import pyrebase
import firebase_admin
from firebase_admin import credentials, db, storage , auth  # Import Firebase Admin SDK
from firebase_admin import auth as firebase_admin_auth
from dotenv import load_dotenv
import os
import pytz
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime

# Initializing flask app
app = Flask(__name__)
# Configure CORS to allow all hosts
CORS(app, resources={r"/*": {"origins": "*"}})
#comment this out if testing in local 
# SECRET_FILE = os.environ.get('SECRET_FILE')
# if SECRET_FILE:
#     with open(SECRET_FILE, 'r') as secret_file:
#         for line in secret_file:
#             line = line.strip()
#             if '=' in line:
#                 key, value = line.split('=', 1)
#                 os.environ[key.strip()] = value.strip()
#             else:
#                 print(f"Skipping line in secret file: {line}")
# uncomment this out if testing in local 
load_dotenv()
database_url = os.getenv("DATABASE_URL")
apiKey = os.getenv("apiKey")
authDomain = os.getenv("authDomain")
projectId = os.getenv("projectId")
storageBucket = os.getenv("storageBucket")
messagingSenderId = os.getenv("messagingSenderId")
appId = os.getenv("appId")
measurementId = os.getenv("measurementId")
debug_mode = os.getenv("DEBUG")
databaseurl = os.getenv("databaseURL")
storagebucket = os.getenv("storageBucket")
twilosid = os.getenv("twiliosid")
twilioauth= os.getenv("twilioauth")
captchaSite= os.getenv("captchaSite")
captchaSecret= os.getenv("captchaSecret")
app_key = os.getenv("APPKEY")

FIREBASE_FILE= os.environ.get('FIREBASE_FILE')

firebase_type = os.getenv("FIREBASE_TYPE")
firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
firebase_private_key_id = os.getenv("FIREBASE_PRIVATE_KEY_ID")
firebase_private_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
firebase_client_id = os.getenv("FIREBASE_CLIENT_ID")
firebase_auth_uri = os.getenv("FIREBASE_AUTH_URI")
firebase_token_uri = os.getenv("FIREBASE_TOKEN_URI")
firebase_auth_provider_cert_url = os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL")
firebase_client_cert_url = os.getenv("FIREBASE_CLIENT_CERT_URL")
firebase_universe_domain = os.getenv("FIREBASE_UNIVERSE_DOMAIN")

# Set Secure Session Cookie Attributes (SECURE, SAMESITE)
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = False

# Set Domain name, ensure no '.' at the start of Cookie
app.config['SESSION_COOKIE_DOMAIN'] = 'priceless-buck.cloud'

# Set Cookie expiration time to 15 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Initialize Firebase Authentication (Unchanged)
config = {
  'apiKey': apiKey,
  'authDomain': authDomain,
  'projectId': projectId,
  'storageBucket': storageBucket,
  'messagingSenderId': messagingSenderId,
  'appId': appId,
  'measurementId': measurementId,
  'databaseURL': ''
}

# Create a Twilio client
client = Client(twilosid, twilioauth)
firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth() 
# Define the maximum number of login attempts allowed

if FIREBASE_FILE is None:
    cred = credentials.Certificate({
  "type": firebase_type,
  "project_id": firebase_project_id,
  "private_key_id": firebase_private_key_id,
  "private_key": firebase_private_key,
  "client_email": firebase_client_email,
  "client_id": firebase_client_id,
  "auth_uri": firebase_auth_uri,
  "token_uri": firebase_token_uri,
  "auth_provider_x509_cert_url": firebase_auth_provider_cert_url,
  "client_x509_cert_url": firebase_client_cert_url,
  "universe_domain": firebase_universe_domain
})
else:
    cred = credentials.Certificate(FIREBASE_FILE)


firebase_admin.initialize_app(cred, {
    'databaseURL': databaseurl,
    'storageBucket': storagebucket
})

# Create a storage reference
storage_ref = storage.bucket()
app.secret_key = app_key