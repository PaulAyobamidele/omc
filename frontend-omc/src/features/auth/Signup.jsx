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
        <div className="flex min-h-screen flex-col justify-center px-6 py-12 lg:px-8 bg-gray-950">
          {/* Heading */}
          <div className="sm:mx-auto sm:w-full sm:max-w-sm">
            <h2 className="mt-8 text-center text-2xl font-bold tracking-tight text-white">
              Create your account
            </h2>
            <p className="mt-2 text-center text-sm text-gray-400">
              Join the platform in seconds
            </p>
          </div>
      
          {/* Form */}
          <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form onSubmit={handleSubmit} className="space-y-6">
      
              {/* Username */}
              <div>
                <label className="block text-sm font-medium text-gray-300">
                  Username
                </label>
                <input
                  name="username"
                  placeholder="Enter username"
                  required
                  className="mt-2 block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2
                             text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
      
              {/* Password */}
              <div>
                <label className="block text-sm font-medium text-gray-300">
                  Password
                </label>
                <input
                  name="password"
                  type="password"
                  placeholder="Enter password"
                  required
                  className="mt-2 block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2
                             text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
      
              {/* First Name */}
              <div>
                <label className="block text-sm font-medium text-gray-300">
                  First Name
                </label>
                <input
                  name="first_name"
                  placeholder="Enter first name"
                  required
                  className="mt-2 block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2
                             text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
      
              {/* Last Name */}
              <div>
                <label className="block text-sm font-medium text-gray-300">
                  Last Name
                </label>
                <input
                  name="last_name"
                  placeholder="Enter last name"
                  required
                  className="mt-2 block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2
                             text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
      
              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-300">
                  Email address
                </label>
                <input
                  name="email"
                  type="email"
                  placeholder="Enter email"
                  required
                  className="mt-2 block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2
                             text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
      
              {/* Role */}
              <div>
                <label className="block text-sm font-medium text-gray-300">
                  Role
                </label>
                <select
                  name="role"
                  required
                  className="mt-2 block w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2
                             text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                >
                  <option value="">Select role</option>
                  <option value="parent">Parent</option>
                  <option value="teacher">Teacher</option>
                </select>
              </div>
      
              {/* Submit */}
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-indigo-600 px-4 py-2
                           text-sm font-semibold text-white hover:bg-indigo-500 focus:ring-2
                           focus:ring-indigo-500 focus:ring-offset-2"
              >
                Sign Up
              </button>
      
              {/* Status Messages */}
              {loading && (
                <p className="text-center text-sm text-gray-400">Creating account...</p>
              )}
      
              {error && (
                <p className="text-center text-sm text-red-400">
                  {JSON.stringify(error)}
                </p>
              )}
            </form>
      
            {/* Already have account? */}
            <p className="mt-6 text-center text-sm text-gray-400">
              Already have an account?{" "}
              <a
                href="/login"
                className="font-semibold text-indigo-400 hover:text-indigo-300"
              >
                Sign in
              </a>
            </p>
          </div>
        </div>
      );
      
}

export default Signup;
