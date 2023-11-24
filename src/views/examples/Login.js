import React from "react";
import {
  Button,
  Card,
  // CardHeader,
  CardBody,
  FormGroup,
  Form,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  // Row,
  Col,
  Row,
  Label,
} from "reactstrap";
import Image  from "../../assets/img/brand/argon-react.png"
// validation
import { userSchema } from "../../firebase/Validation"

// Login
import { LoginSession } from '../../firebase/Authentication'

const Login = () => {

const [showPassword, setShowPassword] = React.useState(false);
const [user, setUser] = React.useState({
  email: "",
  password: ""
})

const [error, setError] = React.useState({
  email: false,
  emailError: "" ,
  password: false,
  passwordError: ""
})

// ****************** SHOW PASSWORD ****************** //
const handleTogglePassword = () => {
  setShowPassword(!showPassword);
};

// ****************** Login Details ****************** //
const handleInputChange = (e) => {
  const { name, value } = e.target;
  setUser((prevUser) => ({
    ...prevUser,
    [name]: value,
  }));
};

// ****************** LOGIN BUTTON ****************** //
const Login = async () =>{
  try {

    await userSchema.validate({ email: user.email, password: user.password }, { abortEarly: false });

    LoginSession(user).then(result=>{
      console.log(result)
    
      setError({
        email: false,
        emailError: "",

        password: false,
        passwordError: ""
      });

    }).catch((error) => {
      console.log("error",error); // Error message

      setError({
        email: true,
        emailError: "",

        password: true,
        passwordError: error
      });
  });


  } catch (validationError) {

    // Extract specific error messages for email and password
    const emailError = validationError.inner.find((error) => error.path === 'email');
    const passwordError = validationError.inner.find((error) => error.path === 'password');

    // If validation errors occur
    setError({
      email: !!emailError,
      emailError: emailError && emailError.message,

      password: !!passwordError,
      passwordError: passwordError && passwordError.message
    });

  }

}


  return (
    <>
      <Col lg="5" md="7">
        <Card className="bg-secondary shadow border-0">
          
          <CardBody className="px-lg-5 py-lg-5">
            <div className="text-center text-muted mb-4">
              <img src={Image} alt="ASD" style={{ width: "150px"}} />

              <p  style={{ color: 'gray' }}>
                All your house controls in one location
              </p>
              
            </div>
            <Form role="form">

            {/* Email */}
              <FormGroup className="mb-3">
                <InputGroup className="input-group-alternative">
                  <InputGroupAddon addonType="prepend">
                    <InputGroupText>
                      <i className="ni ni-email-83" />
                    </InputGroupText>
                  </InputGroupAddon>

                  <Input
                    className={error.email && "text-danger"}
                    placeholder="email"
                    type="text"
                    autoComplete="new-email"
                    name="email"
                    value={user.email}
                    onChange={handleInputChange}
                  />
             
                </InputGroup>
                {error.email && <div className="text-danger mt-1">{error.emailError}</div>}
              </FormGroup>


              {/* Password */}
              <FormGroup  >
                <InputGroup className="input-group-alternative">
                  <InputGroupAddon addonType="prepend">
                    <InputGroupText>
                      <i className="ni ni-lock-circle-open" />
                    </InputGroupText>
                  </InputGroupAddon>
                  <Input
                    className={error.email && "text-danger"}
                    placeholder="Password"
                    autoComplete="new-password"
                    type={showPassword ? 'text' : 'password'} 
                    name="password"
                    value={user.password}
                    onChange={handleInputChange}
                  />
                </InputGroup>
                {error.password && <div className="text-danger mt-1">{error.passwordError}</div>}
              </FormGroup>

 

              {/* Show Password */}
              <FormGroup check inline >
                <Input type="checkbox"  
                id="forgotPasswordCheckbox" 
                checked={showPassword}
                      onChange={handleTogglePassword}
                />
                <Label check for="forgotPasswordCheckbox"> show password </Label>
              </FormGroup>

              <Row className="m-3">
                <Col xs="12">

                  <Button 
                  className="my-4" 
                  color="primary" 
                  type="button" 
                  style={{ minWidth: "100%"}}
                  onClick={Login}>
                    Login
                  </Button>

                </Col>
              </Row>

    
            </Form>
          </CardBody>
        </Card>

        {/* <Row className="mt-3">
          <Col xs="6">
            <a
              className="text-light"
              href="#pablo"
              onClick={(e) => e.preventDefault()}
            >
              <small>Forgot password?</small>
            </a>
          </Col>
          
        </Row> */}

      </Col>
    </>
  );
};

export default Login;
