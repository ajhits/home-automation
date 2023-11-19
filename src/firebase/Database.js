import { onValue, ref, set } from "firebase/database";
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