import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./features/auth/Login.jsx";
import ParentDashboard from "./features/parent/ParentDashboard";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import TeacherDashboard from "./features/teacher/TeacherDashboard";
import Signup from "./features/auth/Signup.jsx";
import EnterGradeForm from "./features/teacher/EnterGrade.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route element={<ProtectedRoute allowedRoles={['PARENT']} />}>
          <Route path="/parent/dashboard" element={<ParentDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['TEACHER']} />}>
          <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
          <Route path="/teacher/enter-grade" element={<EnterGradeForm />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;