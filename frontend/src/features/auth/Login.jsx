import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loginUser, clearError } from "./authSlice";
import { useNavigate, Link, useParams } from "react-router-dom";

export default function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { schoolSlug } = useParams();
  const { loading, error } = useSelector((state) => state.auth);
  const { name: schoolName, logoUrl } = useSelector((state) => state.school);
  const [form, setForm] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (error) dispatch(clearError());
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(loginUser(form))
      .unwrap()
      .then((res) => {
        navigate(`/${schoolSlug}/${res.user.role}/dashboard`);
      })
      .catch(() => {});
  };

  const errorMessage =
    error?.detail || (typeof error === "string" ? error : null);

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
          <p>Modern school management for educators, parents, and students.</p>
        </div>
      </div>

      <div className="auth-form-side">
        <div className="auth-form-wrapper">
          <h2>Sign in</h2>
          <p className="auth-subtitle">Enter your credentials to continue</p>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder="Enter your username"
                required
                autoFocus
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
                placeholder="Enter your password"
                required
              />
            </div>

            {errorMessage && <div className="form-error">{errorMessage}</div>}

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <p className="auth-switch">
            Don&apos;t have an account?{" "}
            <Link to={`/${schoolSlug}/signup`}>Create one</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
