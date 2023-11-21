from Firebase.Firebase import firebaseUpdate,verifiy_rfid


# GPIO PIN SETUP
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


def Lights(name):
    
    print(home_devices[name])
    
    print(f"{name} is open")
    
    

data = verifiy_rfid("rfid")
for key,value in data.items():
    
    
    print(value['TagID'])
    


