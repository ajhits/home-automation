import React from 'react'
import AdminLayout from "layouts/Admin.js";
import AuthLayout from "layouts/Auth.js";
import { 
    Navigate, 
    Route, 
    Routes 
} from 'react-router-dom'

const App = () => {
  return (
    <div>    
        <Routes>
            <Route path="/admin/*" element={<AdminLayout />} />
            <Route path="/auth/*" element={<AuthLayout />} />
            <Route path="*" element={<Navigate to="/auth" replace />} />
        </Routes>
    </div>
  )
}

export default App