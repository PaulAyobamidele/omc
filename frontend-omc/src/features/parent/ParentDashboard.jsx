import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchParentStudents, createStudent } from "../student/studentSlice.jsx";

const ParentDashboard = () => {
  const dispatch = useDispatch();
  const { list: students, loading, error, createLoading, createError } = useSelector(
    (state) => state.students
  );

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    date_of_birth: "",
    class_level: "",
    parent_id: "", // optional, for teachers
  });

  useEffect(() => {
    dispatch(fetchParentStudents());
  }, [dispatch]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(createStudent(form));

    if (result.meta.requestStatus === "fulfilled") {
      alert(`Student created! Username: ${result.payload.username}, Password: ${result.payload.password}`);
      setForm({ first_name: "", last_name: "", date_of_birth: "", class_level: "", parent_id: "" });
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Parent Dashboard</h1>

      <h2>Create New Student</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={form.first_name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={form.last_name}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="date_of_birth"
          placeholder="Date of Birth"
          value={form.date_of_birth}
          onChange={handleChange}
        />
        <input
          type="text"
          name="class_level"
          placeholder="Class Level"
          value={form.class_level}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="parent_id"
          placeholder="Parent ID (Teacher Only)"
          value={form.parent_id}
          onChange={handleChange}
        />

        <button type="submit" disabled={createLoading}>
          {createLoading ? "Creating..." : "Create Student"}
        </button>
        {createError && <p style={{ color: "red" }}>{JSON.stringify(createError)}</p>}
      </form>

      <h2>My Students</h2>
      {loading && <p>Loading students...</p>}
      {error && <p style={{ color: "red" }}>{JSON.stringify(error)}</p>}

      <ul>
        {students.map((student) => (
          <li key={student.student_id || student.id}>
            {student.first_name} {student.last_name} (ID: {student.student_id || student.id})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ParentDashboard;
