import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { getJson } from "../../api/client";
import StatusBadge from "../../components/StatusBadge";
import type { ConflictFlag, PaginatedResponse } from "../../types/api";

function countBySeverity(findings: ConflictFlag[]) {
  return findings.reduce<Record<string, number>>((accumulator, finding) => {
    accumulator[finding.severity] = (accumulator[finding.severity] ?? 0) + 1;
    return accumulator;
  }, {});
}

export default function FindingsDashboardPage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["findings"],
    queryFn: () => getJson<PaginatedResponse<ConflictFlag>>("/api/findings/"),
  });

  if (isLoading) {
    return <div>Loading findings...</div>;
  }

  if (isError) {
    return <div>Failed to load findings: {String(error)}</div>;
  }

  const findings = data?.results ?? [];
  const severityCounts = countBySeverity(findings);

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Findings Dashboard</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          gap: 12,
          marginBottom: 20,
        }}
      >
        {["critical", "high", "medium", "low"].map((severity) => (
          <div key={severity} style={cardStyle}>
            <strong>{severity.toUpperCase()}</strong>
            <div style={{ fontSize: 28, marginTop: 8 }}>{severityCounts[severity] ?? 0}</div>
          </div>
        ))}
      </div>

      <div
        style={{
          backgroundColor: "#ffffff",
          border: "1px solid #e2e8f0",
          borderRadius: 12,
          overflowX: "auto",
        }}
      >
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f8fafc", textAlign: "left" }}>
              <th style={{ padding: 12 }}>ID</th>
              <th style={{ padding: 12 }}>Type</th>
              <th style={{ padding: 12 }}>Severity</th>
              <th style={{ padding: 12 }}>Status</th>
              <th style={{ padding: 12 }}>Summary</th>
            </tr>
          </thead>
          <tbody>
            {findings.map((finding) => (
              <tr key={finding.id} style={{ borderTop: "1px solid #e2e8f0" }}>
                <td style={{ padding: 12 }}>
                  <Link to={`/findings/${finding.id}`}>#{finding.id}</Link>
                </td>
                <td style={{ padding: 12 }}>{finding.conflict_type}</td>
                <td style={{ padding: 12 }}>
                  <StatusBadge value={finding.severity} />
                </td>
                <td style={{ padding: 12 }}>
                  <StatusBadge value={finding.status} />
                </td>
                <td style={{ padding: 12 }}>{finding.reason_summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

const cardStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 16,
};