from app.config.config import db,datetime,pytz,timedelta

# function to get current time
def get_current_time():
    current_time = datetime.now(pytz.utc) + timedelta(hours=8)
    current_time_str = current_time.strftime("%d-%m-%Y %H:%M:%S")

    return current_time_str

# Function to log entries to Firestore under the 'Login_logs' collection with numeric keys
def Login_log_to_DB(entry):
    try:
        # Define the Firestore reference to the 'Login_logs' collection
        login_logs_ref = db.reference('Login_logs')

        # Create a new reference under 'Login_logs' with an automatically generated numeric key
        new_log_ref = login_logs_ref.push()

        # Set the log entry as a key-value pair under the new reference
        new_log_ref.set(entry)

    except Exception as e:
        print("Error logging to Firestore:", str(e))