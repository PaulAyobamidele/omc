import { Link, Navigate, useParams } from "react-router-dom";
import { useSelector } from "react-redux";

export default function Landing() {
  const { schoolSlug } = useParams();
  const { user, accessToken } = useSelector((state) => state.auth);
  const { name: schoolName, logoUrl, address, phone } = useSelector(
    (state) => state.school
  );

  if (accessToken && user) {
    return <Navigate to={`/${schoolSlug}/${user.role}/dashboard`} replace />;
  }

  return (
    <div className="landing">

      {/* ── Nav ── */}
      <nav className="landing-nav">
        <div className="landing-nav-inner">
          <span className="landing-logo">
            {logoUrl ? (
              <img src={logoUrl} alt={schoolName} style={{ height: 28, borderRadius: 4, marginRight: 8, verticalAlign: "middle" }} />
            ) : (
              <span className="landing-logo-icon">▣</span>
            )}
            {schoolName || schoolSlug}
          </span>
          <div className="landing-nav-links">
            <Link to={`/${schoolSlug}/login`} className="btn btn-outline btn-nav">Sign In</Link>
            <Link to={`/${schoolSlug}/signup`} className="btn btn-primary btn-nav">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="landing-hero">
        <div className="landing-container">
          <div className="landing-hero-badge">School Management Platform</div>
          <h1 className="landing-hero-title">
            Welcome to<br />
            <span className="landing-hero-accent">{schoolName || schoolSlug}</span>
          </h1>
          <p className="landing-hero-sub">
            One platform for admins, teachers, parents, and students.
            Track grades, manage classes, and communicate progress — all in one place.
          </p>
          {address && <p style={{ color: "#64748b", marginBottom: 8 }}>{address}</p>}
          {phone && <p style={{ color: "#64748b", marginBottom: 24 }}>Tel: {phone}</p>}
          <div className="landing-hero-cta">
            <Link to={`/${schoolSlug}/signup`} className="btn btn-primary btn-lg">Join School</Link>
            <Link to={`/${schoolSlug}/login`} className="btn btn-ghost btn-lg">Sign In →</Link>
          </div>
        </div>

        <div className="landing-hero-visual">
          <div className="landing-hero-card">
            <div className="lhc-header">
              <span className="lhc-dot red" />
              <span className="lhc-dot amber" />
              <span className="lhc-dot green" />
              <span className="lhc-title">Student Report — JSS 2A</span>
            </div>
            <div className="lhc-body">
              {[
                { subject: "Mathematics", score: 88, max: 100 },
                { subject: "English Language", score: 74, max: 100 },
                { subject: "Basic Science", score: 92, max: 100 },
                { subject: "Social Studies", score: 79, max: 100 },
              ].map((s) => (
                <div className="lhc-row" key={s.subject}>
                  <span className="lhc-subject">{s.subject}</span>
                  <div className="lhc-bar-wrap">
                    <div
                      className="lhc-bar-fill"
                      style={{ width: `${(s.score / s.max) * 100}%` }}
                    />
                  </div>
                  <span className="lhc-score">{s.score}%</span>
                </div>
              ))}
              <div className="lhc-footer">
                <span>Overall</span>
                <span className="lhc-overall">83.25%</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="landing-cta">
        <div className="landing-container landing-cta-inner">
          <h2>Ready to get started?</h2>
          <p>Create your account in seconds. No installation required.</p>
          <div className="landing-hero-cta">
            <Link to={`/${schoolSlug}/signup`} className="btn btn-primary btn-lg">Create an Account</Link>
            <Link to={`/${schoolSlug}/login`} className="btn btn-ghost-light btn-lg">Sign In</Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="landing-footer">
        <div className="landing-container landing-footer-inner">
          <span className="landing-logo">
            {logoUrl ? (
              <img src={logoUrl} alt={schoolName} style={{ height: 20, borderRadius: 3, marginRight: 8, verticalAlign: "middle" }} />
            ) : (
              <span className="landing-logo-icon">▣</span>
            )}
            {schoolName || schoolSlug}
          </span>
          <span className="landing-footer-copy">
            Powered by SchoolHub · © {new Date().getFullYear()}
          </span>
        </div>
      </footer>

    </div>
  );
}
