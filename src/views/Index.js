
import React from "react";

import Header from "components/Headers/Header.js";
import { Card, CardHeader, Container, Row, Table } from "reactstrap";
import { get_the_number_of_shits } from "../firebase/Database";

const Index = () => {


  const [data,setData] = React.useState()
  
  React.useEffect(()=>{
    get_the_number_of_shits()
    .then(data=>{

         // Assuming data is an array of objects with "date" and "time" properties
         const sortedData = Object.values(data.DOOR).sort((a, b) => {
          const dateA = new Date(`${a.date} ${a.time}`);
          const dateB = new Date(`${b.date} ${b.time}`);
          return dateB - dateA; // Sort in descending order (most recent first)
        });

      setData(sortedData)


    })
  },[])


  return (
    <div>
      <Header />
      {/* Page content */}

      <Container className="mt--7" fluid>
      
        {/* Table */}
        <Row>
          <div className="col">
            <Card className="shadow">

              <CardHeader className="border-0">
                <h3 className="mb-0">Entry Log</h3>
              </CardHeader>

              <Table className="align-items-center table-flush" responsive>
                <thead className="thead-light">
                  <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Time</th>
                    <th scope="col">Date</th>
                    <th scope="col" />
                  </tr>
                </thead>
                <tbody>

                  {data && data?.map((user, index) => (
                    <tr key={index}>
                      <td>{user.name}</td>
                      <td>{user.date}</td>
                      <td>{user.time}</td>
                    </tr>
                  ))}

                </tbody>
              </Table>

 

            </Card>



          </div>
        </Row>

      </Container>
    </div>
  );

};

export default Index;
