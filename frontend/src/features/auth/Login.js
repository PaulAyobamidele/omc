import { useDispatch, useSelector } from "react-redux";
import { loginUser } from "./authSlice";
import { useNavigate } from "react-router-dom";

function Login() {

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const { loading, error, user } = useSelector((state) => state.auth);

    const handleSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;

        dispatch(loginUser({ username, password }))
        .unwrap()
        .then((res) => {
            const role = res.user.role.toLowerCase();
            navigate(`/${role}/dashboard`);
        });
        

    };
    return (
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="username" />
        <input name="password" type="password" placeholder="password" />
        <button type="submit">Login</button>

        {loading && <p>Loading...</p>}
        {error && <p>{error.detail}</p>}
      </form>
    )
  }
  
export default Login;