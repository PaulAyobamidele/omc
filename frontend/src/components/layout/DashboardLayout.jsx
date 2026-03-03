import { useState } from "react";
import { Outlet, NavLink, useNavigate, useParams } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../../features/auth/authSlice";

const buildNavItems = (slug) => ({
  parent: [
    { to: `/${slug}/parent/dashboard`, label: "Dashboard", icon: "◉" },
    { to: `/${slug}/parent/children`, label: "My Children", icon: "◎" },
    { to: `/${slug}/parent/grades`, label: "Grades", icon: "◆" },
    { to: `/${slug}/parent/add-child`, label: "Add Child", icon: "◈" },
  ],
  teacher: [
    { to: `/${slug}/teacher/dashboard`, label: "Dashboard", icon: "◉" },
    { to: `/${slug}/teacher/enter-grade`, label: "Enter Grades", icon: "◆" },
    { to: `/${slug}/teacher/classes`, label: "My Classes", icon: "◎" },
    { to: `/${slug}/teacher/students`, label: "Students", icon: "◈" },
  ],
  student: [
    { to: `/${slug}/student/dashboard`, label: "Dashboard", icon: "◉" },
    { to: `/${slug}/student/grades`, label: "My Grades", icon: "◆" },
    { to: `/${slug}/student/report`, label: "Report Card", icon: "◎" },
  ],
  admin: [
    { to: `/${slug}/admin/dashboard`, label: "Dashboard", icon: "◉" },
    { to: `/${slug}/admin/users`, label: "Users", icon: "◎" },
    { to: `/${slug}/admin/classes`, label: "Classes", icon: "◆" },
    { to: `/${slug}/admin/subjects`, label: "Subjects", icon: "◈" },
  ],
});

export default function DashboardLayout() {
  const { user } = useSelector((state) => state.auth);
  const { name: schoolName, logoUrl } = useSelector((state) => state.school);
  const { schoolSlug } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navItems = buildNavItems(schoolSlug);
  const items = navItems[user?.role] || [];

  const handleLogout = () => {
    dispatch(logout());
    navigate(`/${schoolSlug}/login`);
  };

  const roleLabel = user?.role?.charAt(0).toUpperCase() + user?.role?.slice(1);

  return (
    <div className="dashboard-layout">
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div className="logo">
            {logoUrl ? (
              <img src={logoUrl} alt={schoolName} className="logo-img" style={{ height: 28, borderRadius: 4 }} />
            ) : (
              <span className="logo-icon">▣</span>
            )}
            <span className="logo-text">{schoolName || "SchoolHub"}</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
              onClick={() => setSidebarOpen(false)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {user?.first_name?.[0]}
              {user?.last_name?.[0]}
            </div>
            <div className="user-details">
              <span className="user-name">
                {user?.first_name} {user?.last_name}
              </span>
              <span className="user-role">{roleLabel}</span>
            </div>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            Sign Out
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="main-header">
          <button
            className="menu-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰
          </button>
          <div className="header-right">
            <span className="header-greeting">
              Welcome back, {user?.first_name}
            </span>
          </div>
        </header>

        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
