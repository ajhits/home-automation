import threading
import RPi.GPIO as GPIO
import time
from Components.SERVO import move_servo_smoothly,move_two_servos_smoothly
from Firebase.Firebase import get_control_functions

# ***************** PIN SETUP ***************** #
CHRISTMAS_PIN = 12
WINDOW_PIN = 21 # SLIDING WINDOW

# DOOR
DOOR_PIN_1 = 20  # GPIO pin 20
DOOR_PIN_2 = 16  # GPIO pin 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CHRISTMAS_PIN, GPIO.OUT) # CHRISTMAS TREE
GPIO.setup(WINDOW_PIN, GPIO.OUT)    # SLIDING WINDOW
GPIO.setup(DOOR_PIN_1, GPIO.OUT)    # DOOR 1
GPIO.setup(DOOR_PIN_2, GPIO.OUT)    # DOOR 2

# Create PWM instance for the servo
window_servo = GPIO.PWM(WINDOW_PIN, 50)  # 50 Hz frequency

# Start PWM with 0% duty cycle (servo at 0 degrees)
window_servo.start(0)

# Create PWM instances for servos
door_pin_1 = GPIO.PWM(DOOR_PIN_1, 50)  # 50 Hz frequency
door_pin_2 = GPIO.PWM(DOOR_PIN_2, 50)

# Start PWM with 0% duty cycle (servo at 0 degrees)
door_pin_1.start(0)
door_pin_2.start(0)

# ***************** SLIDING WINDOW ***************** #
def set_sliding_window(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    if data:
        move_servo_smoothly(angle=180, servo=window_servo)
        print("window status: ",data)
        return
    print("window status: ", data)
    move_servo_smoothly(angle=0, servo=window_servo)

# ***************** DOOR ***************** #
def set_door_functions(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    if data:
        move_two_servos_smoothly(angle_1=90, angle_2=0, servo_1=door_pin_1,servo_2=door_pin_2)
        time.sleep(3)
        move_two_servos_smoothly(angle_1=0, angle_2=90, servo_1=door_pin_1,servo_2=door_pin_2)
        
    print("door status: ", data)
    
# ***************** CHRISTMAS TREE ***************** #
def christmas_tree(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    print("christmas tree: ", data)
    
    while data:
        if not data:
            break
        
        GPIO.output(CHRISTMAS_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(CHRISTMAS_PIN, GPIO.LOW)
        time.sleep(0.5)

# ***************** CONTROL FUNCTIONS ***************** #
def set_to_control_functions(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    print(name + ": ",data)
    
# ***************** THIS IS THE MAIN FUNCTIONS ***************** # 
def main():
    
    threading.Thread(target=set_door_functions,args=("DOOR",)).start()
    
    threading.Thread(target=christmas_tree,args=("LIGHTS",)).start()
    
    threading.Thread(target=set_sliding_window,args=("WINDOW",)).start()
    set_sliding_window("WINDOW")
    
    return main()
  
if __name__ == '__main__':
    
    main()

    
        


