
import React from "react";

// import Chart from "chart.js";

// import {
//   chartOptions,
//   parseOptions,
//   // chartExample1,
//   // chartExample2,
// } from "variables/charts.js";

import Header from "components/Headers/Header.js";
import { Card, CardHeader, Container, Row, Table } from "reactstrap";
import { get_the_number_of_shits } from "../firebase/Database";

const Index = () => {


  // if (window.Chart) {
  //   parseOptions(Chart, chartOptions());
  // }

  const [data,setData] = React.useState()
  
  React.useEffect(()=>{
    get_the_number_of_shits().then(data=>setData(data.DOOR))
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

                  {data && Object.values(data)?.map((user, index) => (
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
