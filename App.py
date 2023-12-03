import threading
import RPi.GPIO as GPIO
import time
from Firebase.Firebase import get_control_functions, firebaseUpdate,verifiy_rfid, update_history,update_history_door
import socket

import pigpio

from mfrc522 import SimpleMFRC522

#new
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO PIN SETUP
home_devices = {
    'OUT_LIGHTS': 20,
    'LAMP': 18,
    'IN_LIGHTS': 16,
    'WINDOW_1': 26,
    'WINDOW_2': 19,
    'DOOR_PIN_1': 17,
    'DOOR_PIN_2': 27,
    'WATER_PUMP': 21,
    'PET_FEEDER': 12,
    'BUZZER_PIN': 5
}

IR_PIN = 23
LDR_PIN = 24

GPIO.setup(IR_PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)

reader = SimpleMFRC522()



# Setup the Pins
for device_pin in home_devices.values():
    GPIO.setup(device_pin, GPIO.OUT)
    
GPIO.output(home_devices['BUZZER_PIN'], GPIO.LOW)

pwm = pigpio.pi()

# Window Servo
pwm.set_mode(home_devices['WINDOW_1'], pigpio.OUTPUT)
pwm.set_mode(home_devices['WINDOW_2'], pigpio.OUTPUT)

pwm.set_PWM_frequency(home_devices['WINDOW_1'], 50 )
pwm.set_PWM_frequency(home_devices['WINDOW_2'], 50 )

# Door Servo
pwm.set_mode(home_devices['DOOR_PIN_1'], pigpio.OUTPUT)
pwm.set_mode(home_devices['DOOR_PIN_2'], pigpio.OUTPUT)

pwm.set_PWM_frequency(home_devices['DOOR_PIN_1'], 50 )
pwm.set_PWM_frequency(home_devices['DOOR_PIN_2'], 50 )

# Feed Servo
pwm.set_mode(home_devices['PET_FEEDER'], pigpio.OUTPUT)

pwm.set_PWM_frequency(home_devices['PET_FEEDER'], 50 )

# ***************** LDR FUNCTION ***************** # 
def get_light_intensity():
    # Read LDR sensor value (0 for dark, 1 for light)
    return GPIO.input(LDR_PIN)

def control_relay(light_intensity):
    # Control relay based on light intensity
    if light_intensity == 1:  # It's light
        GPIO.output(home_devices['OUT_LIGHTS'], GPIO.HIGH)  # Turn on relay
    else:  # It's dark
        GPIO.output(home_devices['OUT_LIGHTS'], GPIO.LOW)  # Turn off relay
        
def ldr_function():
    
   # Read LDR value
    ldr_value = GPIO.input(LDR_PIN)

    # If LDR value is high (detects light)
    if ldr_value == GPIO.HIGH:
        # Turn on the light
        GPIO.output(home_devices['LAMP'], GPIO.HIGH)
        GPIO.output(home_devices['OUT_LIGHTS'], GPIO.HIGH)
        #print("Light is ON")

    # If LDR value is low (no light)
    else:
        # Turn off the light
        GPIO.output(home_devices['OUT_LIGHTS'], GPIO.LOW)
        GPIO.output(home_devices['LAMP'], GPIO.LOW)
        #print("Light is OFF")

    # Pause for a moment
    # time.sleep(1)

# ***************** BUZZER FUNCTION ***************** # 
def activate_buzzer(duration):
    GPIO.output(home_devices['BUZZER_PIN'], GPIO.HIGH)
    print("Buzzer activated!")
    time.sleep(duration)
    GPIO.output(home_devices['BUZZER_PIN'], GPIO.LOW)
    
# ***************** WINDOW FUNCTION ***************** # 
def move_servo_smoothly(data=None,name=None):
    try:

        # Open The Door
        if data:
                                        
            # Move servo 1 | 180
            pwm.set_servo_pulsewidth(home_devices[name], 2500) ;
            time.sleep( 3 )
        else:
            
            # Move servo 1 | 0
            pwm.set_servo_pulsewidth(home_devices[name], 500) ;
            time.sleep( 3 )
            
    except Exception as e:
        pass
   
def control_window_status(name):

    data = get_control_functions(name)
    move_servo_smoothly(data,name)

# ***************** FEEDER FUNCTION ***************** # 
def feeder_function(data):
    try:

        # Open The Door
        if data:
            
            update_history("PET_FEEDER")
                                        
            # Move servo 1 | 0
            pwm.set_servo_pulsewidth(home_devices['PET_FEEDER'], 500 ) ;
            time.sleep(3)
            firebaseUpdate("PET_FEEDER","data",False)
            
        else:
            
            # Move servo 1 | 90
            pwm.set_servo_pulsewidth(home_devices['PET_FEEDER'], 1500 ) ;

                    
    except Exception as e:
        pass
        # print(f"Error in control_door: {e}")

def control_feeder():
    data = get_control_functions('PET_FEEDER')
    feeder_function(data)
    

    time.sleep(0.3)
    return control_feeder()

# ***************** DOOR FUNCTION ***************** #
def control_door(data):
    try:

        # Open The Door
        if data == True:
            
            # Move servo 1 | 0
            pwm.set_servo_pulsewidth(home_devices['DOOR_PIN_1'], 500) ;

            # Move servo 2 | 90
            pwm.set_servo_pulsewidth(home_devices['DOOR_PIN_2'], 1500) ;
            
            time.sleep(3)
            firebaseUpdate("DOOR","data",False)
        
        else:
            
            # Move servo 1 | 90
            pwm.set_servo_pulsewidth(home_devices['DOOR_PIN_1'], 1600) ;
            time.sleep(0.4)

            # Move servo 2 | 0
            pwm.set_servo_pulsewidth(home_devices['DOOR_PIN_2'], 500) ;

            
    except Exception as e:
        pass
        print(f"Error in control_door: {e}")

def control_door_status():
    
    # Initialize servo for door pin
    data = get_control_functions('DOOR')
    time.sleep(0.2)
    control_door(data)      

# ***************** LIGHTS ***************** #
def control_lights(name):
    
    ldr_value = GPIO.input(LDR_PIN)
    
    if ldr_value == GPIO.HIGH and name == "OUT_LIGHTS":
        return
    

    # get data from firebase
    data = get_control_functions(name)
    
    name == "OUT_LIGHTS" and GPIO.output(home_devices['LAMP'], data)
    GPIO.output(home_devices[name], data)
    
    
    
# ***************** WATER PUMP ***************** #
def control_water_pump():
    try:
        data = get_control_functions('WATER_PUMP')  
        if data:
            GPIO.output(home_devices['WATER_PUMP'], data)
            time.sleep(3)
            GPIO.output(home_devices['WATER_PUMP'], False)
            firebaseUpdate('WATER_PUMP',"data",False)
            
        time.sleep(1)
        return control_water_pump()
    except:
        pass
        time.sleep(1)
        return control_water_pump()

# ***************** RFID ***************** # 
def register_rdfid(register_status, uid):
    if register_status:
        
        # upload the read RFID
        firebaseUpdate(keyName="RFID", child="rf_uid", value=uid)        
        return
    
def read_rfid():
    try:
        print("Hold a tag near the reader")
        id, _ = reader.read()
        return id
    finally:
        print("finally")

# Function to initiate RFID
def rfid_functions():
    
    try:
        
        # Attempt to create a socket connection to a known server (e.g., Google DNS)
        socket.create_connection(("8.8.8.8",53))

        uid = read_rfid()
        print("your RFID: ", uid)
        

        
        # if register is occur
        register = get_control_functions("RFID")
        register_rdfid(register_status=register, uid=uid)
        
        print(register)
        if register:
            activate_buzzer(0.3)
            return rfid_functions()
 
        
        # RFID RESULT
        result = verifiy_rfid(rf_uid=uid)
        
        # IR RESULT
        object_detected = GPIO.input(IR_PIN)
       
        
        activate_buzzer(0.3) if result[1] and object_detected==0 else activate_buzzer(3)

        firebaseUpdate("DOOR","data",result[1] and object_detected==0)
        
        # Updated Code
        result[1] and object_detected == 0 and update_history_door(result[0])
    
        print("Access Granted" if result[1] else "Access Denied")
        
        time.sleep(2)
        
        return rfid_functions()
    except Exception as e:
        pass
        print("Net Failure")
        return rfid_functions()
    
# ***************** Main Function ***************** #  
def main():
    try:
        
        # For control DOOR functions
        control_door_status()
        #threading.Thread(target=control_door_status, args=()).start()
        
        threading.Thread(target=control_window_status, args=('WINDOW_1',)).start()
        time.sleep(0.3)
        threading.Thread(target=control_window_status, args=('WINDOW_2',)).start()
        time.sleep(0.3)
        threading.Thread(target=ldr_function, args=()).start()
           
        # For Controling Lights  
        threading.Thread(target=control_lights, args=('OUT_LIGHTS',)).start()
        time.sleep(0.3)
        threading.Thread(target=control_lights, args=('IN_LIGHTS',)).start()
        
        time.sleep(0.5)
        return main()
    except Exception as e:
        print("No Internet")
        time.sleep(0.5)
        pass
        return main()
            
if __name__ == '__main__':
    print("Smart Home is Running")

        
    threading.Thread(target=rfid_functions, args=()).start()
    threading.Thread(target=control_water_pump, args=()).start()
    
    # For Pet Feeder Function
    threading.Thread(target=control_feeder, args=()).start()
    

    main()

     
