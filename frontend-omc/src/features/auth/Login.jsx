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
      <div className="flex min-h-screen flex-col justify-center px-6 py-12 lg:px-8 bg-gray-950">
        {/* Logo + Heading */}
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <h2 className="mt-8 text-center text-2xl font-bold tracking-tight text-white">
            Sign in to your account
          </h2>
        </div>
    
        {/* Form */}
        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form onSubmit={handleSubmit} className="space-y-6">
    
            {/* Username */}
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-300"
              >
                Username
              </label>
              <div className="mt-2">
                <input
                  id="username"
                  name="username"
                  placeholder="Enter username"
                  required
                  className="block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
            </div>
    
            {/* Password */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-300"
              >
                Password
              </label>
              <div className="mt-2">
                <input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="Enter password"
                  required
                  className="block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
            </div>
    
            {/* Login Button */}
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Login
            </button>
    
            {/* Loading/Error State */}
            {loading && (
              <p className="text-center text-sm text-gray-400">Loading...</p>
            )}
    
            {error && (
              <p className="text-center text-sm text-red-400">{error.detail}</p>
            )}
    
            {/* Signup Link */}
            <p className="text-center text-sm text-gray-400">
              Don’t have an account?{" "}
              <a
                href="/signup"
                className="font-semibold text-indigo-400 hover:text-indigo-300"
              >
                Sign up
              </a>
            </p>
          </form>
    
          {/* Footer Link */}
          <p className="mt-10 text-center text-sm text-gray-500">
            Have a question?{" "}
            <a
              href="#"
              className="font-semibold text-indigo-400 hover:text-indigo-300"
            >
              Write us today!
            </a>
          </p>
        </div>
      </div>
    );
    
    
      }
export default Login;