/*!

=========================================================
* Argon Dashboard React - v1.2.3
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

// reactstrap components
import React from "react";
import { get_the_number_of_shits } from "../../firebase/Database";
import { Card, CardBody, CardTitle, Container, Row, Col } from "reactstrap";

const Header = () => {
  const [door, setDoor] = React.useState(0);
  const [feeding, setFeeding] = React.useState(0);
  const [registered, setRegistered] = React.useState(0);

  const sendTextToTelegram = () => {
    var telegram_bot_id = "6874065354:AAHgmF_sERvDRoMQW0QNBYSY4OPxj7rV3HE";
    var chat_id = 6145248365;
    
    // Get the current date and time in the local timezone
    var currentDate = new Date();
    var formattedDate = currentDate.toLocaleString();
  
    // The text message you want to send
    var textMessage = "Door Opened: " + formattedDate;
  
    // Create a FormData object to send the text message
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
  };
  

  React.useEffect(() => {
    const NumberOfEntries = async () => {
      const data = await get_the_number_of_shits();

      setDoor(Object.values(data.DOOR).length);
      setFeeding(Object.values(data.PET_FEEDER).length);

      // Check if the number of entries has increased (you can adjust the condition based on your logic)
      if (Object.values(data.DOOR).length > door) {
        // Call the function to send a text message to Telegram
        sendTextToTelegram();
      }
    };

    const NumberOfUser = async () => {
      const data = await get_the_number_of_shits("REGISTERED");
      setRegistered(Object.values(data).length);
    };

    NumberOfEntries();
    NumberOfUser();
  }, [door, feeding, registered]);


  return (
    <>
      <div className="header bg-gradient-info pb-8 pt-5 pt-md-8">
        <Container fluid>
          <div className="header-body">
            {/* Card stats */}
            <Row>
              <Col lg="6" xl="3">
                <Card className="card-stats mb-4 mb-xl-0">
                  <CardBody>
                    <Row>
                      <div className="col">
                        <CardTitle
                          tag="h5"
                          className="text-uppercase text-muted mb-0"
                        >
                          Number of Entries
                        </CardTitle>
                        <span className="h2 font-weight-bold mb-0">
                          {door}
                        </span>
                      </div>
                      <Col className="col-auto">
                        <div className="icon icon-shape bg-danger text-white rounded-circle shadow">
                          <i className="fas fa-chart-bar" />
                        </div>
                      </Col>
                    </Row>
                    
                  </CardBody>
                </Card>
              </Col>
              <Col lg="6" xl="3">
                <Card className="card-stats mb-4 mb-xl-0">
                  <CardBody>
                    <Row>
                      <div className="col">
                        <CardTitle
                          tag="h5"
                          className="text-uppercase text-muted mb-0"
                        >
                          Users
                        </CardTitle>
                        <span className="h2 font-weight-bold mb-0">
                          {registered}
                        </span>
                      </div>
                      <Col className="col-auto">
                        <div className="icon icon-shape bg-warning text-white rounded-circle shadow">
                          <i className="fas fa-users" />
                        </div>
                      </Col>
                    </Row>
                    
                  </CardBody>
                </Card>
              </Col>
              <Col lg="6" xl="3">
                <Card className="card-stats mb-4 mb-xl-0">
                  <CardBody>
                    <Row>
                      <div className="col">
                        <CardTitle
                          tag="h5"
                          className="text-uppercase text-muted mb-0"
                        >
                          Feeding Count
                        </CardTitle>
                        <span className="h2 font-weight-bold mb-0">{feeding}</span>
                      </div>
                      <Col className="col-auto">
                        <div className="icon icon-shape bg-yellow text-white rounded-circle shadow">
                          <i className="fas fa-users" />
                        </div>
                      </Col>
                    </Row>
                  
                  </CardBody>
                </Card>
              </Col>
              <Col lg="6" xl="3">
                <Card className="card-stats mb-4 mb-xl-0">
                  <CardBody>
                    <Row>
                      <div className="col">
                        <CardTitle
                          tag="h5"
                          className="text-uppercase text-muted mb-0"
                        >
                          Working Lights
                        </CardTitle>
                        <span className="h3 font-weight-bold mb-0">Outdoor/Indoor</span>
                      </div>
                      <Col className="col-auto">
                        <div className="icon icon-shape bg-info text-white rounded-circle shadow">
                          <i className="fas fa-percent" />
                        </div>
                      </Col>
                    </Row>
                   
                  </CardBody>
                </Card>
              </Col>
            </Row>
          </div>
        </Container>
      </div>
    </>
  );
};

export default Header;
