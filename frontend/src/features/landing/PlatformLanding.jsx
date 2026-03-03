import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const FEATURES = [
  {
    icon: "◈",
    title: "Grade Management",
    desc: "Teachers enter midterm, assignment, and exam scores. Students and parents see results in real time.",
  },
  {
    icon: "◉",
    title: "Parent Dashboard",
    desc: "Parents track every child's academic progress, subject by subject, across all terms.",
  },
  {
    icon: "◎",
    title: "Class Organisation",
    desc: "Admin sets up sessions, terms, and classes once. Teachers fill in subjects and students.",
  },
  {
    icon: "◐",
    title: "Role-Based Access",
    desc: "Each role — admin, teacher, parent, student — sees only what is relevant to them.",
  },
  {
    icon: "◑",
    title: "Detailed Reports",
    desc: "Full academic reports per student, per term. Subject totals, percentages, and overall standing.",
  },
  {
    icon: "◒",
    title: "Custom Branding",
    desc: "Each school gets its own URL, logo, and accent colour. Your school, your identity.",
  },
];

const STEPS = [
  {
    number: "01",
    role: "School Admin",
    title: "Register your school",
    desc: "Sign up in seconds. Get your own school URL like schoolhub.com/yourschool.",
  },
  {
    number: "02",
    role: "Admin",
    title: "Set up classes & terms",
    desc: "Create your academic session, terms, school classes, and assign class teachers.",
  },
  {
    number: "03",
    role: "Everyone",
    title: "Invite your school",
    desc: "Teachers, parents, and students sign in at your school URL and get to work.",
  },
];

export default function PlatformLanding() {
  const navigate = useNavigate();
  const [schoolSlugInput, setSchoolSlugInput] = useState("");

  const handleSlugSearch = (e) => {
    e.preventDefault();
    const slug = schoolSlugInput.trim().toLowerCase().replace(/\s+/g, "-");
    if (slug) navigate(`/${slug}/login`);
  };

  return (
    <div className="landing">

      {/* ── Nav ── */}
      <nav className="landing-nav">
        <div className="landing-nav-inner">
          <span className="landing-logo">
            <span className="landing-logo-icon">▣</span>
            SchoolHub
          </span>
          <div className="landing-nav-links">
            <Link to="/register-school" className="btn btn-primary btn-nav">Register Your School</Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="landing-hero">
        <div className="landing-container">
          <div className="landing-hero-badge">SaaS School Management Platform</div>
          <h1 className="landing-hero-title">
            The smarter way to<br />
            <span className="landing-hero-accent">run your school.</span>
          </h1>
          <p className="landing-hero-sub">
            One platform for every school. Custom URL, custom branding, fully isolated data.
            Sign up your school in seconds — no installation required.
          </p>
          <div className="landing-hero-cta">
            <Link to="/register-school" className="btn btn-primary btn-lg">Register Your School Free</Link>
          </div>

          {/* Already have a school? */}
          <div style={{ marginTop: 32 }}>
            <p style={{ color: "#64748b", marginBottom: 10, fontSize: "0.9rem" }}>
              Already have a school on SchoolHub?
            </p>
            <form onSubmit={handleSlugSearch} style={{ display: "flex", gap: 8, maxWidth: 380 }}>
              <input
                type="text"
                value={schoolSlugInput}
                onChange={(e) => setSchoolSlugInput(e.target.value)}
                placeholder="Enter your school's URL slug"
                style={{
                  flex: 1, padding: "10px 14px", borderRadius: 8,
                  border: "1.5px solid #e2e8f0", fontSize: "0.95rem",
                }}
              />
              <button type="submit" className="btn btn-outline">Go →</button>
            </form>
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

      {/* ── Stats ── */}
      <section className="landing-stats">
        <div className="landing-container landing-stats-inner">
          {[
            { value: "∞", label: "Schools Supported" },
            { value: "4", label: "User Roles" },
            { value: "3", label: "Terms Per Session" },
            { value: "100%", label: "Web-Based" },
          ].map((s) => (
            <div className="landing-stat" key={s.label}>
              <div className="landing-stat-value">{s.value}</div>
              <div className="landing-stat-label">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Features ── */}
      <section className="landing-section" id="features">
        <div className="landing-container">
          <div className="landing-section-header">
            <h2 className="landing-section-title">Everything your school needs</h2>
            <p className="landing-section-sub">
              Built for secondary schools. Each school gets its own isolated, branded space.
            </p>
          </div>
          <div className="landing-features-grid">
            {FEATURES.map((f) => (
              <div className="landing-feature-card" key={f.title}>
                <span className="landing-feature-icon">{f.icon}</span>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="landing-section landing-section-dark" id="how-it-works">
        <div className="landing-container">
          <div className="landing-section-header">
            <h2 className="landing-section-title landing-section-title-light">How it works</h2>
            <p className="landing-section-sub landing-section-sub-light">
              Three steps. One seamless workflow.
            </p>
          </div>
          <div className="landing-steps">
            {STEPS.map((s, i) => (
              <div className="landing-step" key={s.number}>
                <div className="landing-step-number">{s.number}</div>
                <div className="landing-step-content">
                  <span className="landing-step-role">{s.role}</span>
                  <h3>{s.title}</h3>
                  <p>{s.desc}</p>
                </div>
                {i < STEPS.length - 1 && <div className="landing-step-connector" />}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="landing-cta">
        <div className="landing-container landing-cta-inner">
          <h2>Ready to modernise your school?</h2>
          <p>Register in seconds. No installation, no credit card required.</p>
          <div className="landing-hero-cta">
            <Link to="/register-school" className="btn btn-primary btn-lg">Register Your School</Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="landing-footer">
        <div className="landing-container landing-footer-inner">
          <span className="landing-logo">
            <span className="landing-logo-icon">▣</span>
            SchoolHub
          </span>
          <span className="landing-footer-copy">
            © {new Date().getFullYear()} SchoolHub. Built for educators.
          </span>
        </div>
      </footer>

    </div>
  );
}
