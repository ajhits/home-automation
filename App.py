import threading
from Firebase.Firebase import get_control_functions




def set_to_control_functions(name):
    data = get_control_functions(name)
    print(name + ": ",data)



# ***************** THIS IS THE MAIN FUNCTIONS ***************** # 
def main():
    
    threading.Thread(target=set_to_control_functions,args=("DOOR",)).start()
    
    threading.Thread(target=set_to_control_functions,args=("LIGHTS",)).start()
    
    threading.Thread(target=set_to_control_functions,args=("WINDOW",)).start()
  
 
if __name__ == '__main__':
    while True:
        main()
        


