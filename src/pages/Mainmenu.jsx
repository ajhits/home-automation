import React from 'react'
import AuthLayout from "../layouts/Admin";
import { 
    Navigate, 
    Route, 
    Routes 
} from 'react-router-dom';

const Mainmenu = () => {
  return (
    <div>    <Routes>
    <Route path="/admin/*" element={<AuthLayout />} />
    <Route path="*" element={<Navigate to="/admin" replace />} />
  </Routes></div>
  )
}

export default Mainmenu