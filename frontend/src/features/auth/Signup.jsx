import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { signupUser, clearError } from "./authSlice";
import { useNavigate, Link, useParams } from "react-router-dom";

export default function Signup() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { schoolSlug } = useParams();
  const { loading, error } = useSelector((state) => state.auth);
  const { name: schoolName, logoUrl } = useSelector((state) => state.school);

  const [form, setForm] = useState({
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    email: "",
    role: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (error) dispatch(clearError());
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(signupUser(form))
      .unwrap()
      .then((res) => {
        navigate(`/${schoolSlug}/${res.user.role}/dashboard`);
      })
      .catch(() => {});
  };

  const formatError = (err) => {
    if (!err) return null;
    if (typeof err === "string") return err;
    if (err.detail) return err.detail;
    return Object.entries(err)
      .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(", ") : val}`)
      .join(" | ");
  };

  return (
    <div className="auth-page">
      <div className="auth-visual">
        <div className="auth-visual-content">
          {logoUrl ? (
            <img src={logoUrl} alt={schoolName} style={{ height: 64, borderRadius: 8, marginBottom: 16 }} />
          ) : (
            <span className="auth-logo">▣</span>
          )}
          <h1>{schoolName || "SchoolHub"}</h1>
          <p>Join the platform. Manage classes, grades, and reports effortlessly.</p>
        </div>
      </div>

      <div className="auth-form-side">
        <div className="auth-form-wrapper">
          <h2>Create account</h2>
          <p className="auth-subtitle">Get started in seconds</p>

          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="first_name">First Name</label>
                <input
                  id="first_name"
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                  placeholder="First name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="last_name">Last Name</label>
                <input
                  id="last_name"
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                  placeholder="Last name"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="your@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder="Choose a username"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                placeholder="Min. 8 characters"
                required
                minLength={8}
              />
            </div>

            <div className="form-group">
              <label htmlFor="role">I am a...</label>
              <select
                id="role"
                name="role"
                value={form.role}
                onChange={handleChange}
                required
              >
                <option value="">Select your role</option>
                <option value="parent">Parent</option>
                <option value="teacher">Teacher</option>
              </select>
            </div>

            {error && <div className="form-error">{formatError(error)}</div>}

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? "Creating account..." : "Create Account"}
            </button>
          </form>

          <p className="auth-switch">
            Already have an account?{" "}
            <Link to={`/${schoolSlug}/login`}>Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
