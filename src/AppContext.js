import React, { createContext, useContext, useState } from "react";

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [activeLights, setActiveLights] = useState("");

  const updateActiveLights = (newActiveLights) => {
    setActiveLights(newActiveLights);
  };

  return (
    <AppContext.Provider value={{ activeLights, updateActiveLights }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  return useContext(AppContext);
};
