import React, { useState } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  Container,
  Row,
  Col,
  Button,
  // UncontrolledTooltip,
} from "reactstrap";
import Header from "components/Headers/Header.js";

import { control_function,get_control_function } from "../../firebase/Database"; 



const Icons = () => {
  const [buttonStates, setButtonStates] = useState({
    OUT_LIGHTS: false,
    IN_LIGHTS: false,
    WINDOW_1: false,
    WINDOW_2: false,
    DOOR: false,
    WATER_PUMP: false,
    PET_FEEDER: false,
  });

  // Example temperature and humidity values
  const temperature = 25; // in Celsius
  const humidity = 50; // in percentage

  const sendTextToTelegram = () => {
    var telegram_bot_id = "6874065354:AAHgmF_sERvDRoMQW0QNBYSY4OPxj7rV3HE";
    var chat_ids = [6145248365, 1063095169,1120054024]; // Add your additional chat IDs here
    
    // Get the current date and time in the local timezone
    var currentDate = new Date();
    var formattedDate = currentDate.toLocaleString();
    
    // The text message for the alarm activation
    var textMessage = "Alarm Activated: " + formattedDate;
    
    // Iterate over each chat ID and send the message
    chat_ids.forEach(chat_id => {
      // Create a new FormData object for each iteration
      var formData = new FormData();
      formData.append('chat_id', chat_id);
      formData.append('text', textMessage);
  
      // Send the text message to the Telegram Bot API using Ajax
      fetch('https://api.telegram.org/bot' + telegram_bot_id + '/sendMessage', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error(error);
      });
    });
  };
  


  // Define an asynchronous function to fetch and update the state
  const fetchDataAndUpdateState = async () => {
    const updatedStates = {};
    
    // Use Promise.all to wait for all promises to resolve
    await Promise.all(
      Object.entries(buttonStates).map(async ([key]) => {
        const result = await get_control_function(key);
        updatedStates[key] = Boolean(result);
      })
    );

    // Use the functional update form of setButtonStates
    setButtonStates((prevStates) => ({
      ...prevStates,
      ...updatedStates,
    }));

  
  };

  React.useState(()=>{
  

    // Call the function
    fetchDataAndUpdateState();

      // Polling interval, adjust as needed
      const pollingInterval = 1000; // 5 seconds

      const pollingId = setInterval(fetchDataAndUpdateState, pollingInterval);
  
      // Clean up the interval when the component is unmounted
      return () => {
        clearInterval(pollingId);
      };
    
  },[buttonStates])

  const toggleButton = (buttonName) => {

    control_function({
      Name:buttonName, 
      Value:!buttonStates[buttonName]
    })
    

    setButtonStates({
      ...buttonStates,
      [buttonName]: !buttonStates[buttonName],
    });
  };

  return (
    <>
      <Header />
      <Container className="mt--7" fluid>
        <Row>
          <div className="col">
            <Card className="shadow">
              <CardHeader className="bg-transparent">
                <h3 className="mb-0">Manual Controls</h3>
              </CardHeader>
              <CardBody>


                <Row>
                  {/* Lights */}
                  <Col md="3" sm="2" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.OUT_LIGHTS ? "success" : "primary"}
                        onClick={() => toggleButton("OUT_LIGHTS")}
                      >
                        {buttonStates.OUT_LIGHTS ? "On" : "Off"}
                      </Button>
                      <p>Outdoor lights</p>
                    </div>
                  </Col>

                  {/* Door */}
                  <Col md="3" sm="2" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.IN_LIGHTS ? "success" : "primary"}
                        onClick={() => toggleButton("IN_LIGHTS")}
                      >
                        {buttonStates.IN_LIGHTS ? "On" : "Off"}
                      </Button>
                      <p>Indoor lights</p>
                    </div>
                  </Col>

                  {/* Window */}
                  <Col md="3" sm="2" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.WINDOW_1 ? "success" : "primary"}
                        onClick={() => toggleButton("WINDOW_1")}
                      >
                        {buttonStates.WINDOW_1 ? "On" : "Off"}
                      </Button>
                      <p>Window 1</p>
                    </div>
                  </Col>

                  <Col md="3" sm="2" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.WINDOW_2 ? "success" : "primary"}
                        onClick={() => toggleButton("WINDOW_2")}
                      >
                        {buttonStates.WINDOW_2 ? "On" : "Off"}
                      </Button>
                      <p>Window 2</p>
                    </div>
                  </Col>

                </Row>

                {/* ********************** uname functions ***********************/}
                <Row>
                  <Col md="3" sm="2" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.DOOR ? "success" : "primary"}
                        onClick={() => toggleButton("DOOR")}
                      >
                        {buttonStates.DOOR ? "On" : "Off"}
                      </Button>
                      <p>Door</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.WATER_PUMP ? "success" : "primary"}
                        onClick={() => toggleButton("WATER_PUMP")}
                      >
                        {buttonStates.WATER_PUMP ? "On" : "Off"}
                      </Button>
                      <p>Water Pump</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.PET_FEEDER ? "success" : "primary"}
                        onClick={() => toggleButton("PET_FEEDER")}
                      >
                        {buttonStates.PET_FEEDER ? "On" : "Off"}
                      </Button>
                      <p>Pet Feeder</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                    <Button
                     color={buttonStates.ALARM ? "success" : "primary"}
                     onClick={sendTextToTelegram}
                    >
                    Trigger
                    </Button>
                   <p>Alarm</p>
                    </div>
                  </Col>


                  
                 
                </Row>

                {/* Temperature and Humidity */}
                <Row className="mt-4">
                  <Col md="6" xs="12">
                    <div className="text-center">
                      <h4>Temperature: {temperature}°C</h4>
                    </div>
                  </Col>
                  <Col md="6" xs="12">
                    <div className="text-center">
                      <h4>Humidity: {humidity}%</h4>
                    </div>
                  </Col>
                </Row>

              </CardBody>
            </Card>
          </div>
        </Row>
      </Container>
    </>
  );
};

export default Icons;
