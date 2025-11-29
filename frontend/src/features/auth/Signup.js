import { useDispatch, useSelector } from "react-redux";
import { signupUser } from "./authSlice";
import { useNavigate } from "react-router-dom";

function Signup() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { loading, error, user } = useSelector((state) => state.auth);

    const handleSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        const first_name = e.target.first_name.value;
        const last_name = e.target.last_name.value;
        const email = e.target.email.value;
        const role = e.target.role.value; 
        
        dispatch(signupUser({ username, password, first_name, last_name, email, role }))
            .unwrap()
            .then((res) => {
                navigate(`/${res.user.role.toLowerCase()}/dashboard`);
            })
            .catch(() => {});
    };

    return (
        <form onSubmit={handleSubmit}>
            <input name="username" placeholder="Username" required />
            <input name="password" type="password" placeholder="Password" required />
            <input name="first_name" placeholder="First Name" required />
            <input name="last_name" placeholder="Last Name" required />
            <input name="email" type="email" placeholder="Email" required />
            <select name="role" required>
                <option value="">Select Role</option>
                <option value="parent">Parent</option>
                <option value="teacher">Teacher</option>
            </select>
            <button type="submit">Sign Up</button>

            {loading && <p>Loading...</p>}
            {error && <p>{JSON.stringify(error)}</p>}
        </form>
    );
}

export default Signup;
