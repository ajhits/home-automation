import pyrebase
import os
from datetime import datetime



# firebase API keys
config = {
  "apiKey": os.environ.get("REACT_APP_FIREBASE_API_KEY"),
  "authDomain": os.environ.get("REACT_APP_FIREBASE_AUTH_DOMAIN"), 
  "databaseURL": "https://home-automation-4ebbb-default-rtdb.asia-southeast1.firebasedatabase.app", 
  "storageBucket": os.environ.get("REACT_APP_FIREBASE_STORAGE_BUCKET")
}

firebase = pyrebase.initialize_app(config)
db = firebase.database() # realTime database

def get_control_functions(name):
    try:
        data = db.child(name).child("data").get().val()
        
        return data 
        
    except Exception as e:
        print("No Internet")
        return False

# update the current data
def firebaseUpdate(keyName,child, value):
    try:
        db.child(keyName).child(child).set(value)
    except:
        #print("Walang Internet")
        return False 
    finally:

        # print("pumasok sa database")
        return True
      
# verify RID
def verifiy_rfid(rf_uid):
  try:
    data = db.child("REGISTERED").get().val()
    
    for key,value in data.items():
      if value['TagID'] == rf_uid:
          return True
    
    return False
      
        
    

        
  except Exception as e:
    print(f"Error: {e}")
    return False

# **** NOTE: updated Code

# update history
def update_history(keyName):
    
    try:
        # Get current date and time
        now = datetime.now()
    
        # Format the date as 'Month day Year' (e.g., 'Dec 1 2023')
        formatted_date = now.strftime('%b %d %Y')

        # Format the time as 'hour:minute AM/PM' (e.g., '7:16 PM')
        formatted_time = now.strftime('%I:%M %p')
        
        db.child("HISTORY").child(keyName).push(
          {
            "date": str(formatted_date),
            "time": str(formatted_time)                                   
          })
    

    
    except Exception as e:
        print(f"Error: {e}")
        return False
    


