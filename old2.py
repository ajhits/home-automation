import threading
import RPi.GPIO as GPIO
import time
from Components.SERVO import move_servo_smoothly, move_two_servos_smoothly
from Firebase.Firebase import get_control_functions, firebaseUpdate,verifiy_rfid
import socket

from mfrc522 import SimpleMFRC522

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO PIN SETUP
home_devices = {
    'OUT_LIGHTS': 20,
    'IN_LIGHTS': 16,
    'WINDOW_1_PIN': 26,
    'WINDOW_2_PIN': 19,
    'DOOR_PIN_1': 13,
    'DOOR_PIN_2': 6,
    'WATER_PUMP': 21,
    'PET_FEEDER': 12
}

# Setup the Pins
for device_pin in home_devices.values():
    GPIO.setup(device_pin, GPIO.OUT)

# Create PWM instances for servos
window_1_servo = GPIO.PWM(home_devices['WINDOW_1_PIN'], 50)
window_2_servo = GPIO.PWM(home_devices['WINDOW_2_PIN'], 50)

pet_feeder_pin = GPIO.PWM(home_devices['PET_FEEDER'], 50)

# Start PWM
window_1_servo.start(0)
window_2_servo.start(0)

door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)
    
door_pin_1.start(0)
door_pin_2.start(0)

pet_feeder_pin.start(0)

reader = SimpleMFRC522()

def initialize_servo_door():
    door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
    door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)
    
    door_pin_1.start(0)
    door_pin_2.start(0)
# Function to read RFID tags
def read_rfid():
    try:
        print("Hold a tag near the reader")
        id, _ = reader.read()
        return id
    finally:
        print("finally")

# ***************** LIGHTS ***************** #
def control_lights(name):
    
    # get data from firebase
    data = get_control_functions(name)
    GPIO.output(home_devices[name], data)
    
 
# ***************** DOOR ***************** #
def move_servos_smoothly(pos1, pos2):
    # Move servo 1
    duty_cycle1 = pos1 / 18.0 + 2.5
    door_pin_1.ChangeDutyCycle(duty_cycle1)

    # Move servo 2
    duty_cycle2 = pos2 / 18.0 + 2.5
    door_pin_2.ChangeDutyCycle(duty_cycle2)

    time.sleep(1)  # Adjust the sleep time as needed

def door_status(data=None):
    try:
        if data:
            move_servos_smoothly(90,0)
            time.sleep(2)
            move_servos_smoothly(0,90)
            
        door_pin_1.stop()
        door_pin_2.stop()
        
    except Exception as e:
        print(e)
        
def door_status_2(data=None,door_pin_1=None,door_pin_2=None):
    try:
        if data:    
            # Assuming move_servos_smoothly takes door angles as arguments
            move_servos_smoothly(90,0) 
            print("0,90")
            print(data)
            
            time.sleep(3)

          
            move_servos_smoothly(0,90)
            print("0,90")
            print(data)
        # Assuming stop() is the correct method to close the doors
        door_pin_1.stop()
        door_pin_2.stop()
        
    except Exception as e:
        print(e)
    
        # GPIO.cleanup()

        
def control_door(name):
    try:
        data = get_control_functions(name)
        if data:
            door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
            door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)
            
            door_pin_1.start(0)
            door_pin_2.start(0)
            
            door_status_2(data, door_pin_1, door_pin_2)
            
            firebaseUpdate(name, "data", False)
            
            door_pin_1.stop()
            door_pin_2.stop()
        else:
            door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
            door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)
            
            door_pin_1.start(0)
            door_pin_2.start(0)
            
            door_status_2(False, door_pin_1, door_pin_2)
            
            door_pin_1.stop()
            door_pin_2.stop()
            
    except Exception as e:
        print(f"Error in control_door: {e}")

    
# ***************** WINDOWS and PET FEEDER ***************** # 
def control_servo(name, servo, open_angle, close_angle=0, close_delay=None):
    
    # Get data from firebase
    data = get_control_functions(name)

    if data:
        move_servo_smoothly(angle=open_angle, servo=servo)
    
        
        if close_delay is not None:
            time.sleep(close_delay)
            move_servo_smoothly(angle=close_angle, servo=servo)
            print(f"{name} is closed after {close_delay} seconds")
    else:
        move_servo_smoothly(angle=close_angle, servo=servo)
    
# ***************** RFID ***************** # 
def rfid_functions():
    try:
        socket.create_connection(("8.8.8.8",53))
        door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
        door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)

        # Attempt to create a socket connection to a known server (e.g., Google DNS)
        # socket.create_connection(("8.8.8.8", 53))
        
        uid = read_rfid()
        register = get_control_functions("RFID")
        print("your RFID: ", uid)
        
        register_rdfid(register_status=register, uid=uid)
        
        result = verifiy_rfid(rf_uid=uid)
       
        door_pin_1.start(0)
        door_pin_2.start(0)
        
        print("access granted" if result else "access denied")
        door_status(result)
        
        time.sleep(2)
        return rfid_functions()
    except Exception as e:
        print("Net Failure")
        return rfid_functions()
    
def register_rdfid(register_status, uid):
    if register_status:
        firebaseUpdate(keyName="RFID", child="rf_uid", value=uid)        
        return
        
    
def main():
    
    try:

        # Attempt to create a socket connection to a known server (e.g., Google DNS)
        socket.create_connection(("8.8.4.4", 53))
        
        threading.Thread(target=control_lights, args=('OUT_LIGHTS',)).start()
        threading.Thread(target=control_lights, args=('IN_LIGHTS',)).start()
    
        threading.Thread(target=control_door, args=('DOOR',)).start()
    
        # threading.Thread(target=control_servo, args=(
        #    "WINDOW_1",     # name
        #    window_1_servo, # servo
        #    180             # open_angle
        #    )).start()
    
        # window_2 = threading.Thread(target=control_servo, args=(
        #     "WINDOW_2",     # name
        #     window_2_servo, # servo
        #     180             # open_angle
        #     ))
    
        # pet_feeder = threading.Thread(target=control_servo, args=(
        #     "PET_FEEDER",    # name
        #     window_2_servo,  # servo
        #     180,             # open_angle
        #     0,               # close_angle = default 0
        #     3                # close_delay = default None
        #     ))
    
        # window_2.start()
        # pet_feeder.start()
    
        # window_2.join()
        # pet_feeder.join()
        time.sleep(0.5)
        return main()
    except OSError:
        print("No Internet")
        time.sleep(0.5)
        return main()
            


if __name__ == '__main__':
    print("Smart Home is Running")
    
    threading.Thread(target=rfid_functions, args=()).start()
  
    # door_status(False)
    # control_door('DOOR')
    # control_lights('OUT_LIGHTS')
    #rfid_functions()
    
   # main()