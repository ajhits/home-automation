import threading
import RPi.GPIO as GPIO
import time
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
    'WINDOW_1': 26,
    'WINDOW_2': 19,
    'DOOR_PIN_1': 13,
    'DOOR_PIN_2': 6,
    'WATER_PUMP': 21,
    'PET_FEEDER': 12,
    'BUZZER_PIN': 5
}

IR_PIN = 25
LDR_PIN = 24
GPIO.setup(IR_PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP)

reader = SimpleMFRC522()

# Setup the Pins
for device_pin in home_devices.values():
    GPIO.setup(device_pin, GPIO.OUT)
    
GPIO.output(home_devices['BUZZER_PIN'], GPIO.LOW)

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
    light_intensity = get_light_intensity()
    control_relay(light_intensity)
    time.sleep(1)  # Adjust the sleep duration as needed


# ***************** BUZZER FUNCTION ***************** # 
def activate_buzzer(duration):
    GPIO.output(home_devices['BUZZER_PIN'], GPIO.HIGH)
    print("Buzzer activated!")
    time.sleep(duration)
    GPIO.output(home_devices['BUZZER_PIN'], GPIO.LOW)
    
# ***************** WINDOW FUNCTION ***************** # 
def move_servo_smoothly(data=None,name=None):
    try:
        
        # Initialize servo for door pin
        window_pin = GPIO.PWM(home_devices[name], 50)
        window_pin.start(0)

        # Open The Door
        if data:
                                        
            # Move servo 1
            duty_cycle1 = 180 / 18.0 + 2.5
            window_pin.ChangeDutyCycle(duty_cycle1)
            time.sleep(2)
            window_pin.stop(0)
        else:
            # Move servo 1
            duty_cycle1 = 0 / 18.0 + 2.5
            window_pin.ChangeDutyCycle(duty_cycle1)
            time.sleep(2)
            window_pin.stop(0)
            
    except Exception as e:
        pass

    
def control_window_status(name):

    data = get_control_functions(name)
    move_servo_smoothly(data,name)

# ***************** FEEDER FUNCTION ***************** # 
def feeder_function(data):
    try:
        
        # Initialize servo for door pin
        feeder_servo = GPIO.PWM(home_devices['PET_FEEDER'], 50)
  
        feeder_servo.start(0)

        # Open The Door
        if data:
                                        
            # Move servo 1
            duty_cycle1 = 90 / 18.0 + 2.5
            feeder_servo.ChangeDutyCycle(duty_cycle1)

            time.sleep(1)
            feeder_servo.stop(0)
            time.sleep(1)
            firebaseUpdate("PET_FEEDER","data",False)
            
        else:
            
            # Move servo 1
            duty_cycle1 = 0 / 18.0 + 2.5
            feeder_servo.ChangeDutyCycle(duty_cycle1)
            time.sleep(1)
            feeder_servo.stop(0)
                    
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
        
        # Initialize servo for door pin
        door_pin_1 = GPIO.PWM(home_devices['DOOR_PIN_1'], 50)
        door_pin_2 = GPIO.PWM(home_devices['DOOR_PIN_2'], 50)
       
        door_pin_1.start(0)
        door_pin_2.start(0)
        
        # Open The Door
        if data:
                                        
            # Move servo 1
            duty_cycle1 = 90 / 18.0 + 2.5
            door_pin_1.ChangeDutyCycle(duty_cycle1)

            # Move servo 2
            duty_cycle2 = 90 / 18.0 + 2.5
            door_pin_2.ChangeDutyCycle(duty_cycle2)

            time.sleep(1)
            door_pin_1.stop(0)
            door_pin_2.stop(0)
            
            time.sleep(3)
            firebaseUpdate("DOOR","data",False)
            
  
            return
        else:
            
            # Move servo 1
            duty_cycle1 = 0 / 18.0 + 2.5
            door_pin_1.ChangeDutyCycle(duty_cycle1)

            # Move servo 2
            duty_cycle2 = 0 / 18.0 + 2.5
            door_pin_2.ChangeDutyCycle(duty_cycle2)
            
            time.sleep(1)
            
            door_pin_1.stop(0)
            door_pin_2.stop(0)
            

        door_pin_1.stop(0)
        door_pin_2.stop(0)
            
    except Exception as e:
        pass
        # print(f"Error in control_door: {e}")

def control_door_status():
    data = get_control_functions('DOOR')
    control_door(data)

# ***************** LIGHTS ***************** #
def control_lights(name):
    # get data from firebase
    data = get_control_functions(name)
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
        
        # RFID RESULT
        result = verifiy_rfid(rf_uid=uid)
        
        # IRE RESULT
        object_detected = GPIO.input(IR_PIN)
        
        activate_buzzer(0.3) if result else activate_buzzer(3)

        firebaseUpdate("DOOR","data",result)
    
        print("Access Granted" if result else "Access Denied")
        
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
        
        threading.Thread(target=control_window_status, args=('WINDOW_1',)).start()
        threading.Thread(target=control_window_status, args=('WINDOW_2',)).start()
        
        threading.Thread(target=ldr_function, args=()).start()
           
        # For Controling Lights  
        threading.Thread(target=control_lights, args=('OUT_LIGHTS',)).start()
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

    