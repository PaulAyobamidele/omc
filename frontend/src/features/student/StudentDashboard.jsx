import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { gradesApi } from "../../api/services";

export default function StudentDashboard() {
  const { user } = useSelector((state) => state.auth);
  const [grades, setGrades] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  const studentId = user?.profile?.student_id;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const gradesRes = await gradesApi.studentGrades();
      setGrades(gradesRes.data.results || gradesRes.data || []);

      if (studentId) {
        const summaryRes = await gradesApi.studentSummary(studentId);
        setSummary(summaryRes.data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading-state">Loading your grades...</div>;
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>My Dashboard</h1>
        <p className="page-subtitle">
          {user?.profile?.school_class
            ? `Class: ${user.profile.school_class.name}`
            : "Welcome"}
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{grades.length}</div>
          <div className="stat-label">Grades Recorded</div>
        </div>
        {summary && (
          <>
            <div className="stat-card">
              <div className="stat-value">{summary.subjects?.length || 0}</div>
              <div className="stat-label">Subjects</div>
            </div>
            <div className="stat-card accent">
              <div className="stat-value">
                {summary.overall_percentage || 0}%
              </div>
              <div className="stat-label">Overall Average</div>
            </div>
          </>
        )}
      </div>

      {summary?.subjects?.length > 0 && (
        <div className="section">
          <h2>Subject Performance</h2>
          <div className="card-grid">
            {summary.subjects.map((s) => (
              <div key={s.subject_id} className="info-card">
                <h3>{s.subject_name}</h3>
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${Math.min(s.percentage, 100)}%` }}
                  />
                </div>
                <div className="info-card-meta">
                  <span>
                    {s.total_score}/{s.total_max}
                  </span>
                  <span className="font-mono">{s.percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {grades.length > 0 && (
        <div className="section">
          <h2>All Grades</h2>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Category</th>
                  <th>Score</th>
                  <th>Max</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {grades.map((g) => (
                  <tr key={g.id}>
                    <td>{g.subject_name}</td>
                    <td>
                      <span className="badge badge-outline">
                        {g.category_display}
                      </span>
                    </td>
                    <td className="font-mono">{g.score}</td>
                    <td className="text-muted">{g.max_score}</td>
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

