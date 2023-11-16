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

const Icons = () => {
  const [buttonStates, setButtonStates] = useState({
    button1: false,
    button2: false,
    button3: false,
    button4: false,
    button5: false,
    button6: false,
    button7: false,
    button8: false,
  });

  const toggleButton = (buttonName) => {
    setButtonStates({
      ...buttonStates,
      [buttonName]: !buttonStates[buttonName],
    });
  };

  // Example temperature and humidity values
  const temperature = 25; // in Celsius
  const humidity = 50; // in percentage

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
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button1 ? "success" : "primary"}
                        onClick={() => toggleButton("button1")}
                      >
                        {buttonStates.button1 ? "On" : "Off"}
                      </Button>
                      <p>Lights</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button2 ? "success" : "primary"}
                        onClick={() => toggleButton("button2")}
                      >
                        {buttonStates.button2 ? "On" : "Off"}
                      </Button>
                      <p>Door</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button3 ? "success" : "primary"}
                        onClick={() => toggleButton("button3")}
                      >
                        {buttonStates.button3 ? "On" : "Off"}
                      </Button>
                      <p>Window</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button4 ? "success" : "primary"}
                        onClick={() => toggleButton("button4")}
                      >
                        {buttonStates.button4 ? "On" : "Off"}
                      </Button>
                      <p>Another Device</p>
                    </div>
                  </Col>
                </Row>
                <Row>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button5 ? "success" : "primary"}
                        onClick={() => toggleButton("button5")}
                      >
                        {buttonStates.button5 ? "On" : "Off"}
                      </Button>
                      <p>Device 5</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button6 ? "success" : "primary"}
                        onClick={() => toggleButton("button6")}
                      >
                        {buttonStates.button6 ? "On" : "Off"}
                      </Button>
                      <p>Device 6</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button7 ? "success" : "primary"}
                        onClick={() => toggleButton("button7")}
                      >
                        {buttonStates.button7 ? "On" : "Off"}
                      </Button>
                      <p>Device 7</p>
                    </div>
                  </Col>
                  <Col md="3" xs="12">
                    <div className="text-center">
                      <Button
                        color={buttonStates.button8 ? "success" : "primary"}
                        onClick={() => toggleButton("button8")}
                      >
                        {buttonStates.button8 ? "On" : "Off"}
                      </Button>
                      <p>Device 8</p>
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
