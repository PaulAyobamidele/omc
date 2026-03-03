import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { schoolsApi } from "../../api/schoolsApi";
import { loginUser } from "../auth/authSlice";
import { setSlug } from "./schoolSlice";

function toSlug(name) {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-");
}

export default function SchoolRegister() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [form, setForm] = useState({
    school_name: "",
    slug: "",
    primary_color: "#2563eb",
    address: "",
    phone: "",
    school_email: "",
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "school_name") {
      setForm((f) => ({ ...f, school_name: value, slug: toSlug(value) }));
    } else {
      setForm((f) => ({ ...f, [name]: value }));
    }
    setError(null);
  };

  const formatError = (err) => {
    if (!err) return null;
    if (typeof err === "string") return err;
    if (err.detail) return err.detail;
    return Object.entries(err)
      .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : v}`)
      .join(" | ");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await schoolsApi.register(form);

      // Auto-login the new admin
      dispatch(setSlug(form.slug));
      const res = await dispatch(
        loginUser({ username: form.username, password: form.password })
      ).unwrap();

      navigate(`/${form.slug}/${res.user.role}/dashboard`);
    } catch (err) {
      setError(err.response?.data || err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page" style={{ minHeight: "100vh" }}>
      <div className="auth-visual">
        <div className="auth-visual-content">
          <span className="auth-logo">▣</span>
          <h1>SchoolHub</h1>
          <p>Register your school and get your own management platform in seconds.</p>
        </div>
      </div>

      <div className="auth-form-side" style={{ overflowY: "auto", maxHeight: "100vh" }}>
        <div className="auth-form-wrapper" style={{ paddingTop: 32, paddingBottom: 32 }}>
          <h2>Register Your School</h2>
          <p className="auth-subtitle">Fill in your school details to get started</p>

          <form onSubmit={handleSubmit}>
            <p style={{ fontWeight: 600, color: "#0f172a", marginBottom: 8, marginTop: 16 }}>School Details</p>

            <div className="form-group">
              <label>School Name</label>
              <input
                name="school_name"
                value={form.school_name}
                onChange={handleChange}
                placeholder="e.g. Kings College Lagos"
                required
              />
            </div>

            <div className="form-group">
              <label>School URL Slug</label>
              <input
                name="slug"
                value={form.slug}
                onChange={handleChange}
                placeholder="e.g. kings-college-lagos"
                required
                pattern="[a-z0-9-]+"
                title="Lowercase letters, numbers, and hyphens only"
              />
              {form.slug && (
                <small style={{ color: "#64748b" }}>
                  Your login page: <strong>/{form.slug}/login</strong>
                </small>
              )}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Primary Colour</label>
                <input
                  name="primary_color"
                  type="color"
                  value={form.primary_color}
                  onChange={handleChange}
                  style={{ height: 44, cursor: "pointer" }}
                />
              </div>
              <div className="form-group">
                <label>Phone (optional)</label>
                <input
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder="+234 xxx xxx xxxx"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Address (optional)</label>
              <input
                name="address"
                value={form.address}
                onChange={handleChange}
                placeholder="School address"
              />
            </div>

            <div className="form-group">
              <label>School Email (optional)</label>
              <input
                name="school_email"
                type="email"
                value={form.school_email}
                onChange={handleChange}
                placeholder="school@example.com"
              />
            </div>

            <p style={{ fontWeight: 600, color: "#0f172a", marginBottom: 8, marginTop: 24 }}>Admin Account</p>

            <div className="form-row">
              <div className="form-group">
                <label>First Name</label>
                <input
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                  placeholder="First name"
                  required
                />
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <input
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                  placeholder="Last name"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Admin Email</label>
              <input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="admin@yourschool.com"
                required
              />
            </div>

            <div className="form-group">
              <label>Username</label>
              <input
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder="Choose a username"
                required
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <input
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                placeholder="Min. 8 characters"
                required
                minLength={8}
              />
            </div>

            {error && <div className="form-error">{formatError(error)}</div>}

            <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: "100%", marginTop: 8 }}>
              {loading ? "Registering..." : "Register School"}
            </button>
          </form>

          <p className="auth-switch" style={{ marginTop: 16 }}>
            Already registered? <Link to="/">Find your school</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
