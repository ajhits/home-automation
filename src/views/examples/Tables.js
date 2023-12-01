// ... REGISTERED USER ETO

import {
  // Badge,
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Form,
  FormGroup,
  Input,
  Label,
  Pagination,
  // PaginationItem,
  // PaginationLink,
  Table,
  Container,
  Row,
} from "reactstrap";

import Header from "components/Headers/Header.js";

import { control_function } from "../../firebase/Database"; 
import React from "react";
import { 
  get_register_details, 
  set_new_register, 
  update_RFID,
  get_registered_functions,
  delete_registered_user
} from "../../firebase/Database";

const Tables = () => {

  const [req, setReq] = React.useState(false)
  const [tagID,setTagID] = React.useState({
    tagId:""
  })
  const [register,setRegister] = React.useState({
    name: "",
    familiarity: "",
    tagId: ""
  })

  const [registerDetails, setRegisterDetails] = React.useState([]);

  const initiate_rfid = e => {
    e.preventDefault()

    control_function({
      Name: "RFID",
      Value: !req,
    })

    setReq(!req)

    !req === false && update_RFID();

  }

  const updated_tables = async () =>{

    // Fetch registered functions
    const registerDetailsResponse = await get_registered_functions();

    // Extract unique IDs and store data in the state
    const keys = Object.keys(registerDetailsResponse);
    const dataArray = Object.values(registerDetailsResponse).map((item, index) => ({
        id: keys[index],
        ...item,
      }));

    setRegisterDetails(dataArray);

  }


  const fetchData = async () => {
    try {
      // Fetch RFID tag ID
      const tagIdResponse = await get_register_details("RFID");
      setTagID({
        tagId: tagIdResponse.rf_uid,
        data: tagIdResponse.data,
      });
       
      console.log("Data fethed")


    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  React.useEffect(() => {

    updated_tables();


    // Check every second if req is true
    const intervalId = setInterval(() => {
      if (req){
        fetchData();
      }

    }, 200);

    // Clean up the interval on component unmount
    return () => {
      clearInterval(intervalId);
    }

  }, [req,tagID]);


   // Effect for running update_RFID when component unmounts
   React.useEffect(() => {
    return () => {
      update_RFID();
    };
  }, []);


  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRegister((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
  };

  const newRegistered = e => {
    e.preventDefault()

    set_new_register({
      TagID: tagID.tagId,
      Name: register.name,
      Familiarity: register.familiarity
    }).then(e=>{
      update_RFID()

      alert("Registered User")
      
      updated_tables();
      setRegister({
        name: "",
        familiarity: "",
        tagId: ""
      })
      setReq(false)

    })
  }

  const deleteUser = (uid) => {
    delete_registered_user(uid).then(e=>alert(e)).catch(e=>alert(e))
    updated_tables();
  }
  return (
    <>
      <Header />

      {/* Page content */}
      <Container className="mt--7" fluid>

        {/* Table */}
        <Row>
          <div className="col">
            <Card className="shadow">

              <CardHeader className="border-0">
                <h3 className="mb-0">Card tables</h3>
              </CardHeader>

              <Table className="align-items-center table-flush" responsive>
                <thead className="thead-light">
                  <tr>
                    <th scope="col">User ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Familiarity</th>
                    <th scope="col">Action</th>
                    <th scope="col" />
                  </tr>
                </thead>
                <tbody>

                  {registerDetails.map((user, index) => (
                    <tr key={index}>
                      <td>{user.TagID}</td>
                      <td>{user.Name}</td>
                      <td>{user.Familiarity}</td>
                      <td>{         
                        <Button color="warning" size="small" onClick={()=>deleteUser(user.id)}>delete</Button>}</td>
                      {/* Add other columns as needed */}
                    </tr>
                  ))}

                </tbody>
              </Table>

              <CardFooter className="py-4">
                <nav aria-label="...">
                  <Pagination
                    className="pagination justify-content-end mb-0"
                    listClassName="justify-content-end mb-0"
                  >
                    {/* Pagination items... */}
                  </Pagination>
                </nav>
              </CardFooter>

            </Card>

            {/* Button to initiate */}
            <Card className="mt-4 shadow text-center">
            <CardBody>
             <Button color="info" onClick={initiate_rfid} disabled={req}>Initiate RFID</Button>
               <p className="mt-2">
                  {req ? "Please tap your RFID" : "Click this button before trying to input registration to activate the RFID Registration Mode"}
               </p>

               {req && <Button color="warning" onClick={initiate_rfid}>Cancel Registration</Button>}
            </CardBody>
          </Card>

            {/* New section for registration */}
            <Card className="mt-4 shadow">
              <CardHeader className="border-0">
                <h3 className="mb-0">Register New User</h3>
              </CardHeader>
              <CardBody>

                {/* Form for registration */}
                <Form>
                  <FormGroup>
                    <Label for="name">Name</Label>
                    <Input
                      type="text"
                      name="name"
                      id="name"
                      placeholder="Enter name"
                      value={register.name}
                      onChange={handleInputChange}
                    />
                  </FormGroup>

                  <FormGroup>
                    <Label for="familiarity">Familiarity</Label>
                    <Input
                      type="text"
                      name="familiarity"
                      id="familiarity"
                      placeholder="Enter familiarity"
                      value={register.familiarity}
                      onChange={handleInputChange}
                    />
                  </FormGroup>

                  <FormGroup>
                    <Label for="tagId">Tag ID</Label>
                    <Input
                      type="text"
                      name="tagId"
                      id="tagId"
                      placeholder="Tag ID"
                      disabled={true}
                      value={tagID.tagId}
                      // onChange={handleInputChange}
                    />
                  </FormGroup>
                  <Button color="primary" onClick={newRegistered}>Register</Button>
                </Form>
              </CardBody>

            </Card>
          </div>
        </Row>
      </Container>
    </>
  );
};

export default Tables;
