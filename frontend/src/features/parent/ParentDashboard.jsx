import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { gradesApi, studentsApi, classesApi } from "../../api/services";
import { authApi } from "../../api/authApi";

export default function ParentDashboard() {
  const { user } = useSelector((state) => state.auth);
  const [children, setChildren] = useState([]);
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [meRes, gradesRes] = await Promise.all([
        authApi.getMe(),
        gradesApi.parentGrades(),
      ]);
      setChildren(meRes.data.profile?.children || []);
      setGrades(gradesRes.data.results || gradesRes.data || []);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading-state">Loading your dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>Parent Dashboard</h1>
        <p className="page-subtitle">
          Overview of your children's academic progress
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{children.length}</div>
          <div className="stat-label">Children Enrolled</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{grades.length}</div>
          <div className="stat-label">Grade Entries</div>
        </div>
        <div className="stat-card accent">
          <div className="stat-value">
            {children.filter((c) => c.class).length}
          </div>
          <div className="stat-label">Assigned to Classes</div>
        </div>
      </div>

      <div className="section">
        <h2>My Children</h2>
        {children.length === 0 ? (
          <div className="empty-state">
            <p>No children registered yet.</p>
            <a href="/parent/add-child" className="btn btn-primary">
              Add Your First Child
            </a>
          </div>
        ) : (
          <div className="card-grid">
            {children.map((child) => (
              <div key={child.id} className="info-card">
                <div className="info-card-header">
                  <div className="avatar">{child.name?.[0]}</div>
                  <div>
                    <h3>{child.name}</h3>
                    <span className="badge">{child.class || "No Class"}</span>
                  </div>
                </div>
                <div className="info-card-actions">
                  <a
                    href={`/parent/grades?student=${child.id}`}
                    className="btn btn-sm"
                  >
                    View Grades
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {grades.length > 0 && (
        <div className="section">
          <h2>Recent Grades</h2>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Subject</th>
                  <th>Category</th>
                  <th>Score</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {grades.slice(0, 10).map((g) => (
                  <tr key={g.id}>
                    <td>{g.student_name}</td>
                    <td>{g.subject_name}</td>
                    <td>
                      <span className="badge badge-outline">
                        {g.category_display}
                      </span>
                    </td>
                    <td className="font-mono">
                      {g.score}/{g.max_score}
                    </td>
                    <td className="text-muted">
                      {new Date(g.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}