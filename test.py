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

# Iterating through keys and values
for key, value in home_devices.items():
    print(key, ":", value)