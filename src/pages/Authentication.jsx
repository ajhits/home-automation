import React from 'react'
import AuthLayout from "../layouts/Auth";
import { Navigate, Route, Routes } from 'react-router-dom';

const Authentication = () => {
  return (
    <div>    <Routes>

    <Route path="/auth/*" element={<AuthLayout />} />
    <Route path="*" element={<Navigate to="/auth" replace />} />
  </Routes></div>
  )
}

export default Authentication