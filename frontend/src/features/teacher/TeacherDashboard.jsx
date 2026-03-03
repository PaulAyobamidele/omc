import { useState, useEffect } from "react";
import { teachersApi, subjectsApi, classesApi, studentsApi, parentsApi } from "../../api/services";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";

export default function TeacherDashboard() {
  const { user } = useSelector((state) => state.auth);
  const teacherId = user?.profile?.teacher_id;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Add Subject form
  const [subjects, setSubjects] = useState([]);
  const [subjectForm, setSubjectForm] = useState({ school_class: "", subject: "" });
  const [subjectMsg, setSubjectMsg] = useState(null);
  const [subjectLoading, setSubjectLoading] = useState(false);

  // Add Student form
  const [parents, setParents] = useState([]);
  const [parentSearch, setParentSearch] = useState("");
  const [studentForm, setStudentForm] = useState({
    first_name: "", last_name: "", date_of_birth: "", school_class_id: "", parent_id: "",
  });
  const [studentMsg, setStudentMsg] = useState(null);
  const [studentLoading, setStudentLoading] = useState(false);

  const refreshDashboard = () => {
    return teachersApi.dashboard().then((res) => setData(res.data));
  };

  useEffect(() => {
    refreshDashboard()
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
    subjectsApi.list().then((res) => setSubjects(res.data.results || res.data || []));
  }, []);

  useEffect(() => {
    const timeout = setTimeout(() => {
      parentsApi.list({ search: parentSearch }).then((res) =>
        setParents(res.data.results || res.data || [])
      );
    }, 300);
    return () => clearTimeout(timeout);
  }, [parentSearch]);

  const handleAddSubject = async (e) => {
    e.preventDefault();
    setSubjectLoading(true);
    setSubjectMsg(null);
    try {
      await classesApi.createClassSubject({
        school_class: parseInt(subjectForm.school_class),
        subject: parseInt(subjectForm.subject),
        teacher: teacherId,
      });
      setSubjectMsg({ type: "success", text: "Subject added to class." });
      setSubjectForm({ school_class: "", subject: "" });
      refreshDashboard();
    } catch (err) {
      setSubjectMsg({
        type: "error",
        text: err.response?.data?.detail || err.response?.data?.non_field_errors?.[0] || "Failed to add subject.",
      });
    } finally {
      setSubjectLoading(false);
    }
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    setStudentLoading(true);
    setStudentMsg(null);
    try {
      const payload = {
        first_name: studentForm.first_name,
        last_name: studentForm.last_name,
        school_class_id: parseInt(studentForm.school_class_id),
        parent_id: parseInt(studentForm.parent_id),
      };
      if (studentForm.date_of_birth) payload.date_of_birth = studentForm.date_of_birth;

      const res = await studentsApi.create(payload);
      setStudentMsg({
        type: "success",
        text: `Student created. Username: ${res.data.username} | Password: ${res.data.password}`,
      });
      setStudentForm({ first_name: "", last_name: "", date_of_birth: "", school_class_id: "", parent_id: "" });
    } catch (err) {
      const errData = err.response?.data;
      const msg = errData?.detail || errData?.parent_id?.[0] || JSON.stringify(errData) || "Failed to add student.";
      setStudentMsg({ type: "error", text: msg });
    } finally {
      setStudentLoading(false);
    }
  };

  if (loading) return <div className="loading-state">Loading dashboard...</div>;
  if (!data) return <div className="empty-state">Unable to load dashboard data.</div>;

  const managedClasses = data.classes_managed || [];

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>Teacher Dashboard</h1>
        <p className="page-subtitle">Welcome back, {data.name}</p>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{managedClasses.length}</div>
          <div className="stat-label">Classes Managed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.subjects_teaching?.length || 0}</div>
          <div className="stat-label">Subjects Teaching</div>
        </div>
        <div className="stat-card accent">
          <Link to="/teacher/enter-grade" className="stat-action">Enter Grades →</Link>
          <div className="stat-label">Quick Action</div>
        </div>
      </div>

      {/* Classes I Manage */}
      {managedClasses.length > 0 && (
        <div className="section">
          <h2>Classes I Manage</h2>
          <div className="card-grid">
            {managedClasses.map((cls) => (
              <div key={cls.id} className="info-card">
                <h3>{cls.name}</h3>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Subjects I Teach */}
      {data.subjects_teaching?.length > 0 && (
        <div className="section">
          <h2>Subjects I Teach</h2>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr><th>Class</th><th>Subject</th><th>Action</th></tr>
              </thead>
              <tbody>
                {data.subjects_teaching.map((cs) => (
                  <tr key={cs.id}>
                    <td>{cs.class}</td>
                    <td>{cs.subject}</td>
                    <td>
                      <Link to={`/teacher/enter-grade?class_subject=${cs.id}`} className="btn btn-sm">
                        Enter Grade
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Setup section — only shown if teacher manages at least one class */}
      {managedClasses.length > 0 && (
        <div className="section">
          <h2>Setup</h2>
          <div className="card-grid">

            {/* Add Subject to Class */}
            <div className="form-card">
              <h3>Register Subject for Class</h3>
              <form onSubmit={handleAddSubject}>
                <div className="form-group">
                  <label>Class</label>
                  <select
                    value={subjectForm.school_class}
                    onChange={(e) => setSubjectForm({ ...subjectForm, school_class: e.target.value })}
                    required
                  >
                    <option value="">Select class</option>
                    {managedClasses.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Subject</label>
                  <select
                    value={subjectForm.subject}
                    onChange={(e) => setSubjectForm({ ...subjectForm, subject: e.target.value })}
                    required
                  >
                    <option value="">Select subject</option>
                    {subjects.map((s) => (
                      <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                </div>
                {subjectMsg && (
                  <div className={`form-message ${subjectMsg.type}`}>{subjectMsg.text}</div>
                )}
                <button type="submit" className="btn btn-primary" disabled={subjectLoading}>
                  {subjectLoading ? "Adding..." : "Add Subject"}
                </button>
              </form>
            </div>

            {/* Add Student */}
            <div className="form-card">
              <h3>Add Student</h3>
              <form onSubmit={handleAddStudent}>
                <div className="form-row">
                  <div className="form-group">
                    <label>First Name</label>
                    <input
                      value={studentForm.first_name}
                      onChange={(e) => setStudentForm({ ...studentForm, first_name: e.target.value })}
                      placeholder="First name"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Last Name</label>
                    <input
                      value={studentForm.last_name}
                      onChange={(e) => setStudentForm({ ...studentForm, last_name: e.target.value })}
                      placeholder="Last name"
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>Date of Birth (optional)</label>
                  <input
                    type="date"
                    value={studentForm.date_of_birth}
                    onChange={(e) => setStudentForm({ ...studentForm, date_of_birth: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Class</label>
                  <select
                    value={studentForm.school_class_id}
                    onChange={(e) => setStudentForm({ ...studentForm, school_class_id: e.target.value })}
                    required
                  >
                    <option value="">Select class</option>
                    {managedClasses.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Parent (search by name or username)</label>
                  <input
                    value={parentSearch}
                    onChange={(e) => setParentSearch(e.target.value)}
                    placeholder="Type to search parents..."
                  />
                  <select
                    value={studentForm.parent_id}
                    onChange={(e) => setStudentForm({ ...studentForm, parent_id: e.target.value })}
                    required
                  >
                    <option value="">Select parent</option>
                    {parents.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.full_name} (@{p.username})
                      </option>
                    ))}
                  </select>
                </div>
                {studentMsg && (
                  <div className={`form-message ${studentMsg.type}`} style={{ wordBreak: "break-all" }}>
                    {studentMsg.text}
                  </div>
                )}
                <button type="submit" className="btn btn-primary" disabled={studentLoading}>
                  {studentLoading ? "Adding..." : "Add Student"}
                </button>
              </form>
            </div>

          </div>
        </div>
      )}

      {managedClasses.length === 0 && (
        <div className="empty-state">
          You have not been assigned to manage any class yet. Contact your admin.
        </div>
      )}
    </div>
  );
}