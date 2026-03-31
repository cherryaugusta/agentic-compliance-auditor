import { useQuery } from "@tanstack/react-query";

import { getJson } from "../../api/client";
import type { ConflictMetrics, OverviewMetrics, ReviewOpsMetrics } from "../../types/api";

function MetricCard({ label, value }: { label: string; value: number | string }) {
  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        border: "1px solid #e2e8f0",
        borderRadius: 12,
        padding: 16,
      }}
    >
      <div style={{ color: "#475569", fontSize: 14 }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 700, marginTop: 8 }}>{value}</div>
    </div>
  );
}

export default function MetricsPage() {
  const overviewQuery = useQuery({
    queryKey: ["metrics-overview"],
    queryFn: () => getJson<OverviewMetrics>("/api/metrics/overview/"),
  });

  const reviewOpsQuery = useQuery({
    queryKey: ["metrics-review-ops"],
    queryFn: () => getJson<ReviewOpsMetrics>("/api/metrics/review-ops/"),
  });

  const conflictsQuery = useQuery({
    queryKey: ["metrics-conflicts"],
    queryFn: () => getJson<ConflictMetrics>("/api/metrics/conflicts/"),
  });

  if (overviewQuery.isLoading || reviewOpsQuery.isLoading || conflictsQuery.isLoading) {
    return <div>Loading metrics...</div>;
  }

  if (overviewQuery.isError || reviewOpsQuery.isError || conflictsQuery.isError) {
    return <div>Failed to load metrics.</div>;
  }

  const overview = overviewQuery.data;
  const reviewOps = reviewOpsQuery.data;
  const conflicts = conflictsQuery.data;

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Metrics Overview</h2>
      <p style={{ color: "#475569" }}>
        Aggregated audit workflow metrics, review operations, and degraded-mode visibility.
      </p>

      <h3>Overview</h3>
      <div style={gridStyle}>
        <MetricCard label="Documents" value={overview?.documents ?? 0} />
        <MetricCard label="Comparison Runs" value={overview?.comparison_runs ?? 0} />
        <MetricCard label="Findings" value={overview?.findings ?? 0} />
        <MetricCard label="Review Tasks" value={overview?.review_tasks ?? 0} />
        <MetricCard label="Eval Runs" value={overview?.eval_runs ?? 0} />
      </div>

      <h3>Review Operations</h3>
      <div style={gridStyle}>
        <MetricCard label="Unassigned" value={reviewOps?.unassigned ?? 0} />
        <MetricCard label="Assigned" value={reviewOps?.assigned ?? 0} />
        <MetricCard label="In Review" value={reviewOps?.in_review ?? 0} />
        <MetricCard label="Approved" value={reviewOps?.approved ?? 0} />
        <MetricCard label="Dismissed" value={reviewOps?.dismissed ?? 0} />
        <MetricCard label="Escalated" value={reviewOps?.escalated ?? 0} />
      </div>

      <h3>Conflict Metrics</h3>
      <div style={gridStyle}>
        <MetricCard label="Open" value={conflicts?.open ?? 0} />
        <MetricCard label="Needs Review" value={conflicts?.needs_review ?? 0} />
        <MetricCard label="Confirmed" value={conflicts?.confirmed ?? 0} />
        <MetricCard label="Dismissed" value={conflicts?.dismissed ?? 0} />
        <MetricCard label="Escalated" value={conflicts?.escalated ?? 0} />
        <MetricCard label="Resolved" value={conflicts?.resolved ?? 0} />
        <MetricCard label="Degraded Runs" value={conflicts?.degraded_runs ?? 0} />
      </div>
    </section>
  );
}

const gridStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
  gap: 12,
  marginBottom: 24,
};