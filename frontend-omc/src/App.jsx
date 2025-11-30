import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./features/auth/Login.jsx";
import ParentDashboard from "./features/parent/ParentDashboard";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import TeacherDashboard from "./features/teacher/TeacherDashboard";
import Signup from "./features/auth/Signup.jsx";

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
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;