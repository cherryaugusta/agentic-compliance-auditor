import { Link, NavLink, Outlet } from "react-router-dom";

const navItems = [
  ["/", "Documents"],
  ["/lineage", "Lineage"],
  ["/comparisons/new", "Comparisons"],
  ["/findings", "Findings"],
  ["/review-queue", "Review Queue"],
  ["/metrics", "Metrics"],
  ["/evals", "Evals"],
  ["/admin-tools", "Admin"],
] as const;

function navStyle(isActive: boolean) {
  return {
    textDecoration: "none",
    padding: "8px 12px",
    borderRadius: 8,
    border: "1px solid #cbd5e1",
    backgroundColor: isActive ? "#e2e8f0" : "#ffffff",
    color: "#0f172a",
    fontWeight: 600,
  };
}

export default function AppLayout() {
  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f8fafc",
        color: "#0f172a",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <header
        style={{
          borderBottom: "1px solid #e2e8f0",
          backgroundColor: "#ffffff",
        }}
      >
        <div
          style={{
            maxWidth: 1200,
            margin: "0 auto",
            padding: "20px 24px",
          }}
        >
          <Link
            to="/"
            style={{
              textDecoration: "none",
              color: "#0f172a",
            }}
          >
            <h1 style={{ margin: 0, fontSize: 28 }}>Agentic Compliance Auditor</h1>
          </Link>
          <p style={{ margin: "8px 0 0 0", color: "#475569" }}>
            Rules-first, AI-assisted policy-control audit workflow
          </p>
          <nav
            style={{
              display: "flex",
              gap: 12,
              flexWrap: "wrap",
              marginTop: 16,
            }}
          >
            {navItems.map(([to, label]) => (
              <NavLink key={to} to={to} style={({ isActive }) => navStyle(isActive)}>
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main
        style={{
          maxWidth: 1200,
          margin: "0 auto",
          padding: 24,
        }}
      >
        <Outlet />
      </main>
    </div>
  );
}