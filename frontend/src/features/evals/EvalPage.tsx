import { useQuery } from "@tanstack/react-query";

import { getJson } from "../../api/client";
import type { EvalReport } from "../../types/api";

export default function EvalPage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["eval-report-latest"],
    queryFn: () => getJson<EvalReport>("/api/evals/runs/reports/latest/"),
  });

  if (isLoading) {
    return <div>Loading eval report...</div>;
  }

  if (isError) {
    return <div>Failed to load eval report: {String(error)}</div>;
  }

  const metrics = [
    ["Contradiction Precision", data?.contradiction_precision],
    ["Contradiction Recall", data?.contradiction_recall],
    ["Stale Reference Accuracy", data?.stale_reference_accuracy],
    ["Citation Validity Rate", data?.citation_validity_rate],
    ["Review Routing Accuracy", data?.review_routing_accuracy],
  ] as const;

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Latest Eval Report</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 12,
          marginTop: 20,
        }}
      >
        {metrics.map(([label, value]) => (
          <div key={label} style={cardStyle}>
            <div style={{ color: "#475569", fontSize: 14 }}>{label}</div>
            <div style={{ fontSize: 28, fontWeight: 700, marginTop: 8 }}>
              {value ?? 0}
            </div>
          </div>
        ))}
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