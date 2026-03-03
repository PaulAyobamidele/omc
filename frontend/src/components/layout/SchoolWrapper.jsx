import { useEffect } from "react";
import { useParams, Outlet, Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { setSlug, fetchSchoolPublic } from "../../features/schools/schoolSlice";

export default function SchoolWrapper() {
  const { schoolSlug } = useParams();
  const dispatch = useDispatch();
  const { name, primaryColor, loading, error } = useSelector((state) => state.school);

  useEffect(() => {
    if (schoolSlug) {
      dispatch(setSlug(schoolSlug));
      dispatch(fetchSchoolPublic(schoolSlug));
    }
  }, [schoolSlug, dispatch]);

  useEffect(() => {
    if (primaryColor) {
      document.documentElement.style.setProperty("--accent", primaryColor);
    }
  }, [primaryColor]);

  if (error) return <Navigate to="/" replace />;

  if (loading || !name) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", fontSize: "1rem", color: "#64748b" }}>
        Loading school…
      </div>
    );
  }

  return <Outlet />;
}
