import { useEffect } from "react";
import { useNavigate } from "react-router";

function Logout() {
  const navigate = useNavigate();
  useEffect(() => {
    const apiCall = async () => {
      try {
        console.log(localStorage.getItem("accessToken"));
        const url = "http://127.0.0.1:5000/auth/logout";
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("accessToken"),
          },
        });
        const data = await response.json();
        console.log(data);
        localStorage.removeItem("accessToken");
        navigate("/");
      } catch (error) {
        console.log("Error: ", error);
        navigate("/");
      }
    };
    if (localStorage.getItem("accessToken") == null) {
      navigate("/");
    } else {
      apiCall();
    }
  }, []);
  return <></>;
}

export default Logout;
