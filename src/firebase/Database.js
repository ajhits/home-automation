import { onValue, push, ref, set } from "firebase/database";
import { RTdb } from "./Configuration";

// **************** CONTROL FUNCTIONS **************** //
export const control_function = async (props) => {
    try {
        const keyRef = ref(RTdb, `${props.Name}/data/`);
        
        set(keyRef,props.Value);

 
    } catch (err) {
        console.error(err);
    }
}

// **************** GET STATUS OF CONTROL FUNCTIONS  **************** //
export const get_control_function = (Name) => {
    const keyRef = ref(RTdb, `${Name}/data`);
  
    return new Promise((resolve, reject) => {
      onValue(keyRef, (snapshot) => {
        const data = snapshot.val();
        resolve(data)
      }, (error) => {
        reject(error);
      });
    });
    
  }

// **************** REGISTER FUNCTIONS  **************** //
export const get_register_details = (name) => {
  const keyRef = ref(RTdb,name);
  
  return new Promise((resolve, reject) => {
    onValue(keyRef, (snapshot) => {
      const data = snapshot.val();
      resolve(data)
    }, (error) => {
      reject(error);
    });
  });
}

export const set_new_register = (props) => {
  return new Promise((resolve, reject) => {
    try {
      const keyRef = ref(RTdb, 'REGISTERED/');

      // Use push to generate a unique ID for the new item
      const newChildRef = push(keyRef);

      // Set the data at the generated child location
      set(newChildRef, props);

      resolve('data created');
    } catch (err) {
      reject(err);
    }
  });
};

export const update_RFID = async () => {
  try {
      const keyRef = ref(RTdb, `RFID`);
      
      set(keyRef,{
        data: false,
        rf_uid: ""
      });


  } catch (err) {
      console.error(err);
  }
}