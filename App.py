import threading
import RPi.GPIO as GPIO
import time
from Components.SERVO import move_servo_smoothly,move_two_servos_smoothly
from Firebase.Firebase import get_control_functions

# ***************** GPIO PIN SETUP ***************** #
home_devices = {
    'OUTDOOR_LIGHTS': 20,
    'INDOOR_LIGHTS': 16,
    'WINDOW_1_PIN': 26,
    'WINDOW_2_PIN': 19,
    'DOOR_PIN_1': 13,
    'DOOR_PIN_2': 6,
    'WATER_PUMP': 21,
    'PET_FEEDER': 12
}

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# setup the Pins
for key, value in home_devices.items():
    GPIO.setup(value, GPIO.OUT) # CHRISTMAS TREE

# Create PWM instances for servos in windows
window_1_servo = GPIO.PWM(home_devices['WINDOW_1_PIN'], 50)  # 50 Hz frequency
window_2_servo = GPIO.PWM(home_devices['WINDOW_2_PIN'], 50)  # 50 Hz frequency

window_1_servo.start(0)
window_2_servo.start(0)

# Create PWM instances for servos in DOOR
door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)  # 50 Hz frequency
door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)

door_pin_1.start(0)
door_pin_2.start(0)

# Create PWM instances for servos in pet feeder
pet_feeder_pin = GPIO.PWM(home_devices['PET_FEEDER'], 50)
pet_feeder_pin.start(0)

# ***************** SLIDING WINDOWS ***************** #
def set_window_1(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    if data:
        move_servo_smoothly(angle=180, servo=window_1_servo)
        return

    move_servo_smoothly(angle=0, servo=window_1_servo)
    
def set_window_2(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    if data:
        move_servo_smoothly(angle=180, servo=window_2_servo)
        return
    
    move_servo_smoothly(angle=0, servo=window_2_servo)

# ***************** DOOR ***************** #
def set_door_functions(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    if data:
        move_two_servos_smoothly(angle_1=90, angle_2=0, 
                                 servo_1=door_pin_1,servo_2=door_pin_2)
        time.sleep(3)
        move_two_servos_smoothly(angle_1=0, angle_2=90, servo_1=door_pin_1,servo_2=door_pin_2)
        
# ***************** OUTDOOR LIGHTS ***************** #
def outdoor_lights(name):
    
    # get data from firebase
    data = get_control_functions(name)
    GPIO.output(home_devices['OUTDOOR_LIGHTS'], data)
    
def indoor_lights(name):
    
    # get data from firebase
    data = get_control_functions(name)
    GPIO.output(home_devices['INDOOR_LIGHTS'], data)
    
# ***************** WATER PUMP ***************** #    
def water_pumps(name):
    
    # get data from firebase
    data = get_control_functions(name)
    if data:
        GPIO.output(home_devices['WATER_PUMP'], GPIO.HIGH)
        time.sleep(4)
        GPIO.output(home_devices['WATER_PUMP'], GPIO.LOW)
        
# ***************** PET FEEDER ***************** #         
def pet_feeder(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    if data:
        move_servo_smoothly(angle=0, servo=pet_feeder_pin)
        time.sleep(3)
        move_servo_smoothly(angle=90, servo=pet_feeder_pin)
        
    
# ***************** CONTROL FUNCTIONS ***************** #
def set_to_control_functions(name):
    
    # get data from firebase
    data = get_control_functions(name)
    
    
# ***************** THIS IS THE MAIN FUNCTIONS ***************** # 
def main():
    threading.Thread(target=outdoor_lights, args=("OUT_LIGHTS",)).start()
    threading.Thread(target=outdoor_lights, args=("IN_LIGHTS",)).start()
    
    set_window_1("WINDOW_1")
    set_window_1("WINDOW_2")
    
    threading.Thread(target=set_door_functions, args=("DOOR",)).start()
    threading.Thread(target=water_pumps, args=("WATER_PUMP",)).start()
    
    pet_feeder("PET_FEEDER")
    
    return main()
  
if __name__ == '__main__':
    print("Smart Home is Running")
    main()

    
        


