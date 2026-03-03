import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PlatformLanding from "./features/landing/PlatformLanding";
import SchoolWrapper from "./components/layout/SchoolWrapper";
import Landing from "./features/landing/Landing";
import Login from "./features/auth/Login";
import Signup from "./features/auth/Signup";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import DashboardLayout from "./components/layout/DashboardLayout";
import ParentDashboard from "./features/parent/ParentDashboard";
import AddChild from "./features/parent/AddChild";
import TeacherDashboard from "./features/teacher/TeacherDashboard";
import EnterGrade from "./features/teacher/EnterGrade";
import StudentDashboard from "./features/student/StudentDashboard";
import SchoolRegister from "./features/schools/SchoolRegister";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Platform root */}
        <Route path="/" element={<PlatformLanding />} />
        <Route path="/register-school" element={<SchoolRegister />} />

        {/* All school-specific routes under /:schoolSlug */}
        <Route path="/:schoolSlug" element={<SchoolWrapper />}>
          <Route index element={<Landing />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />

          {/* Parent routes */}
          <Route element={<ProtectedRoute allowedRoles={["parent"]} />}>
            <Route element={<DashboardLayout />}>
              <Route path="parent/dashboard" element={<ParentDashboard />} />
              <Route path="parent/add-child" element={<AddChild />} />
              <Route path="parent/children" element={<ParentDashboard />} />
              <Route path="parent/grades" element={<ParentDashboard />} />
            </Route>
          </Route>

          {/* Teacher routes */}
          <Route element={<ProtectedRoute allowedRoles={["teacher"]} />}>
            <Route element={<DashboardLayout />}>
              <Route path="teacher/dashboard" element={<TeacherDashboard />} />
              <Route path="teacher/enter-grade" element={<EnterGrade />} />
              <Route path="teacher/classes" element={<TeacherDashboard />} />
              <Route path="teacher/students" element={<TeacherDashboard />} />
            </Route>
          </Route>

          {/* Student routes */}
          <Route element={<ProtectedRoute allowedRoles={["student"]} />}>
            <Route element={<DashboardLayout />}>
              <Route path="student/dashboard" element={<StudentDashboard />} />
              <Route path="student/grades" element={<StudentDashboard />} />
              <Route path="student/report" element={<StudentDashboard />} />
            </Route>
          </Route>

          {/* Admin routes */}
          <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
            <Route element={<DashboardLayout />}>
              <Route path="admin/dashboard" element={<div>Admin Dashboard (coming soon)</div>} />
            </Route>
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
