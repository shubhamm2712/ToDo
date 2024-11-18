import { useState } from "react";
import { Alert, Button, Col, Container, Form, Row } from "react-bootstrap";
import { useNavigate } from "react-router";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [alertMessage, setAlertMessage] = useState("");
  const login = async () => {
    setUsername(username.trim());
    setPassword(password.trim());
    if (username === "" || password === "") {
      setAlertMessage("Missing Values");
    }
    const url = "http://127.0.0.1:5000/auth/login";
    try {
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({ username: username, password: password }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      if (response.status == 400 || response.status == 500) {
        setAlertMessage(data["message"]);
      } else if (response.status != 200) {
        setAlertMessage("Check logs");
        console.log(response);
      } else {
        var accessToken = data["access_token"];
        localStorage.setItem("accessToken", accessToken);
        navigate("/dashboard");
      }
    } catch (error) {
      console.log("Error");
      console.log(error);
    }
  };
  return (
    <>
      <Container fluid>
        <Row>
          <Col></Col>
          <Col md={4}>
            <Form>
              <Form.Group>
                <label className="me-3">Username </label>
                <input
                  type="text"
                  name="username"
                  onChange={(e) => {
                    setUsername(e.target.value);
                  }}
                ></input>
              </Form.Group>

              <Form.Group>
                <label className="me-3">Password </label>
                <input
                  type="password"
                  name="password"
                  id="password"
                  onChange={(e) => {
                    setPassword(e.target.value);
                  }}
                ></input>
              </Form.Group>

              <Button className="primary mt-4" onClick={login}>
                Submit
              </Button>
            </Form>
            {alertMessage && (
              <Alert className="alert-danger mt-3">{alertMessage}</Alert>
            )}
          </Col>
          <Col></Col>
        </Row>
      </Container>
    </>
  );
}

export default Login;
