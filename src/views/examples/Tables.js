// ...

import {
  Badge,
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
  PaginationItem,
  PaginationLink,
  Table,
  Container,
  Row,
} from "reactstrap";

import Header from "components/Headers/Header.js";

const Tables = () => {
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
                    <th scope="col">Tag Status</th>
                    <th scope="col" />
                  </tr>
                </thead>
                <tbody>
                  {/* Add your table rows here */}
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
             <Button color="info">Initiate RFID</Button>
               <p className="mt-2">
                Click this button before trying to input registration to activate the RFID Registration Mode
               </p>
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
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label for="familiarity">Familiarity</Label>
                    <Input
                      type="text"
                      name="familiarity"
                      id="familiarity"
                      placeholder="Enter familiarity"
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label for="tagId">Tag ID</Label>
                    <Input
                      type="text"
                      name="tagId"
                      id="tagId"
                      placeholder="Tag ID"
                    />
                  </FormGroup>
                  <Button color="primary">Register</Button>
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
