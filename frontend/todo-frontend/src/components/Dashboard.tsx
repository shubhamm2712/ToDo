import { useEffect } from "react";
import { useNavigate } from "react-router";

function Dashboard() {
  const navigate = useNavigate();

  var accessToken = "";
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token !== null) {
      accessToken = token;
    } else {
      navigate("/");
    }
  }, []);
  return <>Dashboard</>;
}

export default Dashboard;
