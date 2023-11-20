# power 3.3v
#RST - GPIO22
#GND-GND
#MISO - GPIO9
#MOSI - GPIO10 
#SCK - GPIO11
#SDA - GPIO8


from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)

reader = SimpleMFRC522()

# Function to read RFID tags
def read_rfid():
    try:
        print("Hold a tag near the reader")
        id, _ = reader.read()
        return id
    finally:
        GPIO.cleanup()

# Main loop to continuously read RFID tags
# while True:
#     try:
#         uid = read_rfid()
#         if uid:
#             print("RFID card detected!")
#             # Replace the following UID with your allowed UID
#             allowed_uid = 487492232216   # Replace this with your allowed UID
#             if uid == allowed_uid:
#                 print("Access granted!")
#             else:
#                 print("Access denied!")
#         sleep(2)  # Sleep for a while before the next read
#     except KeyboardInterrupt:
#         print("\nCtrl+C captured, exiting.")
#         GPIO.cleanup()





