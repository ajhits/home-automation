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
import React from "react";
// node.js library that concatenates classes (strings)
// import classnames from "classnames";
// javascipt plugin for creating charts
import Chart from "chart.js";
// // react plugin used to create charts
// import { Line, Bar } from "react-chartjs-2";
// // reactstrap components
// import {
//   Button,
//   Card,
//   CardHeader,
//   CardBody,
//   NavItem,
//   NavLink,
//   Nav,
//   Progress,
//   Table,
//   Container,
//   Row,
//   Col,
// } from "reactstrap";

// core components
import {
  chartOptions,
  parseOptions,
  // chartExample1,
  // chartExample2,
} from "variables/charts.js";

import Header from "components/Headers/Header.js";
import { Card, CardHeader, Row, Table } from "reactstrap";

const Index = (props) => {
  // const [activeNav, setActiveNav] = useState(1);
  // const [chartExample1Data, setChartExample1Data] = useState("data1");

  if (window.Chart) {
    parseOptions(Chart, chartOptions());
  }

  // const toggleNavs = (e, index) => {
  //   e.preventDefault();
  //   setActiveNav(index);
  //   setChartExample1Data("data" + index);
  // };

  return (
    <>
      <Header />
      {/* Page content */}
      
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
                    <th scope="col">Date and Time</th>
                    <th scope="col" />
                  </tr>
                </thead>
                <tbody>

                  {/* {registerDetails.map((user, index) => (
                    <tr key={index}>
                      <td>{user.TagID}</td>
                      <td>{user.Name}</td>
                      <td>{user.Familiarity}</td>
                      <td>{         
                        <Button color="warning" size="small" onClick={()=>deleteUser(user.id)}>delete</Button>}</td>

                    </tr>
                  ))} */}

                </tbody>
              </Table>

 

            </Card>



          </div>
        </Row>
    </>
  );
};

export default Index;
