// src/components/layout/ProtectedRoute.js
import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

const ProtectedRoute = ({ allowedRoles }) => {
  const { user, accessToken } = useSelector((state) => state.auth);

  if (!accessToken || !user) return <Navigate to="/login" replace />;

  const userRole = user.role?.toUpperCase();

  if (!allowedRoles.includes(userRole)) return <Navigate to="/login" replace />;

  return <Outlet />;
};


export default ProtectedRoute;
