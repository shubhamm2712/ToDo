import { useState } from "react";
import { Alert, Button, Col, Container, FormGroup, Row } from "react-bootstrap";
import { Form, useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [alertMessage, setAlertMessage] = useState("");

  const handleSubmit = async () => {
    try {
      const url = "http://127.0.0.1:5000/auth/register";
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
          name: name,
        }),
      });
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        alert("Successfully added");
        navigate("/");
      } else {
        setAlertMessage(data["message"]);
      }
    } catch (error) {
      console.log("Error: ", error);
    }
  };

  return (
    <>
      <Container fluid>
        <Row>
          <Col></Col>
          <Col md={6}>
            <Form>
              <FormGroup>
                <label>Username</label>
                <input
                  type="text"
                  onChange={(e) => {
                    setUsername(e.target.value);
                  }}
                ></input>
              </FormGroup>

              <FormGroup>
                <label>Password</label>
                <input
                  type="password"
                  onChange={(e) => {
                    setPassword(e.target.value);
                  }}
                ></input>
              </FormGroup>

              <FormGroup>
                <label>Name</label>
                <input
                  type="text"
                  onChange={(e) => {
                    setName(e.target.value);
                  }}
                ></input>
              </FormGroup>

              <Button
                className="btn-primary"
                type="submit"
                onClick={handleSubmit}
              >
                Submit
              </Button>
            </Form>

            {alertMessage && (
              <Alert className="alert-danger">{alertMessage}</Alert>
            )}
          </Col>
          <Col></Col>
        </Row>
      </Container>
    </>
  );
}

export default Register;
