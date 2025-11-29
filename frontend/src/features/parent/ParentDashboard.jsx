import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchParentStudents } from './parentApi';

const ParentDashboard = () => {
  const navigate = useNavigate();


  const user = useSelector((state) => state.auth.user);

  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    async function loadStudents() {
      try {
        const data = await fetchParentStudents();
        setStudents(data);
      } catch (err){
        console.error('Failed to fetch students:', err);
      } finally {
        setLoading(false);
      }
    }
    loadStudents();
  }, []);

  if (loading) return <p>Loading dashboard...</p>;

  return (
    <div>
      <h1>Welcome, {user?.name}</h1>
      <h2>Your Children:</h2>
      {students.length === 0 ? (
        <p>No children linked to your account.</p>
      ) : (
        <ul>
          {students.map((student) => (
            <li key={student.id}>
              <strong>{student.first_name} {student.last_name}</strong>
              <button onClick={() => navigate(`/parent/student/${student.id}/report`)}>View Report Card
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};


export default ParentDashboard;