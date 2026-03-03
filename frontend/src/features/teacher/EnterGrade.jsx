import { useState, useEffect } from "react";
import { gradesApi, classesApi, studentsApi } from "../../api/services";
import { useSearchParams } from "react-router-dom";

const CATEGORIES = [
  { value: "MIDTERM", label: "Midterm Test", max: 20 },
  { value: "ASSIGNMENT1", label: "Assignment 1", max: 10 },
  { value: "ASSIGNMENT2", label: "Assignment 2", max: 10 },
  { value: "EXAM", label: "Final Exam", max: 60 },
];

export default function EnterGrade() {
  const [searchParams] = useSearchParams();
  const [classSubjects, setClassSubjects] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState(null);
  const [message, setMessage] = useState(null);

  const [form, setForm] = useState({
    student: "",
    class_subject: searchParams.get("class_subject") || "",
    category: "",
    score: "",
  });

  useEffect(() => {
    classesApi.classSubjects()
      .then((res) => {
        setClassSubjects(res.data.results || res.data || []);
      })
      .catch((err) => {
        setLoadError(err.response?.data?.detail || "Failed to load classes.");
      });
  }, []);

  useEffect(() => {
    if (form.class_subject) {
      const cs = classSubjects.find(
        (c) => c.id === parseInt(form.class_subject)
      );
      if (cs) {
        studentsApi.byClass(cs.school_class)
          .then((res) => {
            setStudents(res.data.results || res.data || []);
          })
          .catch(() => setStudents([]));
      }
    } else {
      setStudents([]);
    }
  }, [form.class_subject, classSubjects]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setMessage(null);
  };

  const selectedCategory = CATEGORIES.find((c) => c.value === form.category);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      await gradesApi.enter({
        student: parseInt(form.student),
        class_subject: parseInt(form.class_subject),
        category: form.category,
        score: parseFloat(form.score),
      });
      setMessage({ type: "success", text: "Grade submitted successfully." });
      setForm({ ...form, student: "", category: "", score: "" });
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        err.response?.data?.non_field_errors?.[0] ||
        JSON.stringify(err.response?.data) ||
        "Failed to submit grade";
      setMessage({ type: "error", text: detail });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>Enter Grade</h1>
        <p className="page-subtitle">Submit a grade for a student</p>
      </div>

      {loadError && <div className="form-message error">{loadError}</div>}

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="class_subject">Class — Subject</label>
            <select
              id="class_subject"
              name="class_subject"
              value={form.class_subject}
              onChange={handleChange}
              required
            >
              <option value="">Select class & subject</option>
              {classSubjects.map((cs) => (
                <option key={cs.id} value={cs.id}>
                  {cs.school_class_name} — {cs.subject_name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="student">Student</label>
            <select
              id="student"
              name="student"
              value={form.student}
              onChange={handleChange}
              required
              disabled={!form.class_subject}
            >
              <option value="">
                {form.class_subject
                  ? "Select a student"
                  : "Select class first"}
              </option>
              {students.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.full_name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="category">Category</label>
              <select
                id="category"
                name="category"
                value={form.category}
                onChange={handleChange}
                required
              >
                <option value="">Select category</option>
                {CATEGORIES.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label} (max {c.max})
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="score">
                Score{" "}
                {selectedCategory && (
                  <span className="text-muted">/ {selectedCategory.max}</span>
                )}
              </label>
              <input
                id="score"
                name="score"
                type="number"
                step="0.01"
                min="0"
                max={selectedCategory?.max || 100}
                value={form.score}
                onChange={handleChange}
                placeholder="0"
                required
              />
            </div>
          </div>

          {message && (
            <div className={`form-message ${message.type}`}>
              {message.text}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Submitting..." : "Submit Grade"}
          </button>
        </form>
      </div>
    </div>
  );
}

