import threading
import RPi.GPIO as GPIO
import time
from Components.SERVO import move_servo_smoothly, move_two_servos_smoothly
from Firebase.Firebase import get_control_functions

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

door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)

pet_feeder_pin = GPIO.PWM(home_devices['PET_FEEDER'], 50)

# Start PWM
window_1_servo.start(0)
window_2_servo.start(0)

door_pin_1.start(0)
door_pin_2.start(0)

pet_feeder_pin.start(0)

reader = SimpleMFRC522()

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
def door_status(open):
    
    if open:
        move_two_servos_smoothly(angle_1=90, angle_2=0, servo_1=door_pin_1,servo_2=door_pin_2)
        time.sleep(3)
        move_two_servos_smoothly(angle_1=0, angle_2=90, servo_1=door_pin_1,servo_2=door_pin_2)
        
def control_door(name):
    
    # get data from firebase
    data = get_control_functions(name)
    door_status(data)

    
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
        uid = read_rfid()
        print("your RFID: ", uid)
        time.sleep(2)
        return rfid_functions()
    except:
        return rfid_functions()
    
def main():

    threading.Thread(target=control_lights, args=('OUT_LIGHTS',)).start()
    threading.Thread(target=control_lights, args=('IN_LIGHTS',)).start()
    
    threading.Thread(target=control_door, args=('DOOR',)).start()
    
    # threading.Thread(target=control_servo, args=(
    #     "WINDOW_1",     # name
    #     window_1_servo, # servo
    #     180             # open_angle
    #     )).start()
    
    # window_2 = threading.Thread(target=control_servo, args=(
    #     "WINDOW_2",     # name
    #     window_2_servo, # servo
    #     180             # open_angle
    #     )).start()
    
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
    
    return main()


if __name__ == '__main__':
    print("Smart Home is Running")
    
    threading.Thread(target=rfid_functions, args=()).start()
    
    main()