import React from 'react'

import Authentication from 'pages/Authentication';
import Mainmenu from 'pages/Mainmenu';
import { statusLogin } from './firebase/Authentication';

const App = () => {
  const [isAuthenticated, setAuthenticated] =  React.useState()

  React.useEffect(()=>{

  // Check the status login
  statusLogin()
    .then(user=>
      { 
        user !== null ? setAuthenticated("authenticated") : setAuthenticated("login") 
      })

  },[isAuthenticated])

  return (
    <div>    
      {isAuthenticated === "login" && <Authentication />}
      {isAuthenticated === "authenticated" && <Mainmenu />}
    </div>
  )
}





export default App