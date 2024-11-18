import { useEffect } from "react";
import { useNavigate } from "react-router";

function Home() {
  const navigate = useNavigate();
  useEffect(() => {
    if (
      localStorage.getItem("accessToken") != null &&
      localStorage.getItem("accessToken") != undefined
    ) {
      navigate("/dashboard");
    }
  }, []);
  return <>Welcome to ToDo list</>;
}

export default Home;
