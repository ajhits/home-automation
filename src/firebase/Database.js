import { ref, set } from "firebase/database";
import { RTdb } from "./Configuration";

// **************** cONTROL FUNCTIONS **************** //
export const control_function = async (props) => {
    try {
        const keyRef = ref(RTdb, `${props.Name}/data/`);
        
        set(keyRef,props.Value);

 
    } catch (err) {
        console.error(err);
    }
}