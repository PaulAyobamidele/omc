import { Navigate, Outlet, useParams } from "react-router-dom";
import { useSelector } from "react-redux";

const ProtectedRoute = ({ allowedRoles }) => {
  const { user, accessToken } = useSelector((state) => state.auth);
  const { schoolSlug } = useParams();

  if (!accessToken || !user) {
    return <Navigate to={`/${schoolSlug}/login`} replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to={`/${schoolSlug}/login`} replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
