import { useSelector } from "react-redux";
import { useEffect } from "react";

function DebugAuth() {
  const auth = useSelector(state => state.auth);

  useEffect(() => {
    console.log("Redux auth state:", auth);
  }, [auth]);

  return null;
}

export default DebugAuth;
