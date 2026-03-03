import { useState, useEffect } from "react";
import { studentsApi, classesApi } from "../../api/services";
import { useNavigate } from "react-router-dom";

export default function AddChild() {
  const navigate = useNavigate();
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    date_of_birth: "",
    school_class_id: "",
  });

  useEffect(() => {
    classesApi.list().then((res) => {
      setClasses(res.data.results || res.data || []);
    });
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await studentsApi.create({
        ...form,
        school_class_id: parseInt(form.school_class_id),
      });
      setResult(res.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          JSON.stringify(err.response?.data) ||
          "Failed to create student"
      );
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="dashboard">
        <div className="page-header">
          <h1>Child Created Successfully</h1>
        </div>
        <div className="result-card">
          <div className="result-icon">✓</div>
          <h3>
            {result.first_name} {result.last_name}
          </h3>
          <div className="credentials">
            <div className="credential-row">
              <span className="credential-label">Username</span>
              <code>{result.username}</code>
            </div>
            <div className="credential-row">
              <span className="credential-label">Password</span>
              <code>{result.password}</code>
            </div>
            <div className="credential-row">
              <span className="credential-label">Class</span>
              <span>{result.school_class}</span>
            </div>
          </div>
          <p className="warning-text">
            Save these credentials — the password cannot be retrieved later.
          </p>
          <div className="result-actions">
            <button
              className="btn btn-primary"
              onClick={() => {
                setResult(null);
                setForm({ first_name: "", last_name: "", date_of_birth: "", school_class_id: "" });
              }}
            >
              Add Another Child
            </button>
            <button
              className="btn btn-outline"
              onClick={() => navigate("/parent/dashboard")}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>Add a Child</h1>
        <p className="page-subtitle">Register a new student under your account</p>
      </div>

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                id="first_name"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
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
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="date_of_birth">Date of Birth</label>
            <input
              id="date_of_birth"
              name="date_of_birth"
              type="date"
              value={form.date_of_birth}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="school_class_id">Class</label>
            <select
              id="school_class_id"
              name="school_class_id"
              value={form.school_class_id}
              onChange={handleChange}
              required
            >
              <option value="">Select a class</option>
              {classes.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {error && <div className="form-error">{error}</div>}

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Creating..." : "Create Student Account"}
          </button>
        </form>
      </div>
    </div>
  );
}