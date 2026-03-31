import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";

import { getJson } from "../../api/client";
import StatusBadge from "../../components/StatusBadge";
import type { ConflictFlag, EvidenceCitation, FindingMemo } from "../../types/api";

export default function FindingDetailPage() {
  const params = useParams();
  const id = params.id;

  const findingQuery = useQuery({
    queryKey: ["finding", id],
    queryFn: () => getJson<ConflictFlag>(`/api/findings/${id}/`),
    enabled: Boolean(id),
  });

  const citationsQuery = useQuery({
    queryKey: ["finding-citations", id],
    queryFn: () => getJson<EvidenceCitation[]>(`/api/findings/${id}/citations/`),
    enabled: Boolean(id),
  });

  const memoQuery = useQuery({
    queryKey: ["finding-memo", id],
    queryFn: () => getJson<FindingMemo | null>(`/api/findings/${id}/memo/`),
    enabled: Boolean(id),
  });

  if (findingQuery.isLoading || citationsQuery.isLoading || memoQuery.isLoading) {
    return <div>Loading finding detail...</div>;
  }

  if (findingQuery.isError || citationsQuery.isError || memoQuery.isError) {
    return <div>Failed to load finding detail.</div>;
  }

  const finding = findingQuery.data;
  const citations = citationsQuery.data ?? [];
  const memo = memoQuery.data;

  if (!finding) {
    return <div>Finding not found.</div>;
  }

  const sourceCitations = citations.filter((citation) => citation.citation_role === "source");
  const targetCitations = citations.filter((citation) => citation.citation_role === "target");
  const contextCitations = citations.filter((citation) => citation.citation_role === "context");

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Finding #{finding.id}</h2>

      <div
        style={{
          display: "flex",
          gap: 12,
          flexWrap: "wrap",
          marginBottom: 20,
        }}
      >
        <StatusBadge value={finding.conflict_type} />
        <StatusBadge value={finding.severity} />
        <StatusBadge value={finding.status} />
      </div>

      <div style={panelStyle}>
        <strong>Summary</strong>
        <p>{finding.reason_summary}</p>
        <div>
          <strong>Confidence:</strong> {finding.confidence}
        </div>
        <div>
          <strong>Rules Triggered:</strong> {finding.rules_triggered.join(", ")}
        </div>
        <div style={{ marginTop: 12 }}>
          <a href={`http://localhost:8000/api/findings/${finding.id}/export_packet/`} target="_blank" rel="noreferrer">
            Export finding packet
          </a>
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: 16,
          marginTop: 20,
        }}
      >
        <div style={panelStyle}>
          <h3 style={{ marginTop: 0 }}>Source Citations</h3>
          {sourceCitations.length === 0 ? <p>None</p> : sourceCitations.map(renderCitation)}
        </div>

        <div style={panelStyle}>
          <h3 style={{ marginTop: 0 }}>Target Citations</h3>
          {targetCitations.length === 0 ? <p>None</p> : targetCitations.map(renderCitation)}
        </div>

        <div style={panelStyle}>
          <h3 style={{ marginTop: 0 }}>Context Citations</h3>
          {contextCitations.length === 0 ? <p>None</p> : contextCitations.map(renderCitation)}
        </div>
      </div>

      <div style={panelStyle}>
        <h3 style={{ marginTop: 0 }}>Memo</h3>
        {memo ? (
          <>
            <div>
              <strong>Recommended Action:</strong> {memo.recommended_action}
            </div>
            <div>
              <strong>Confidence:</strong> {memo.confidence}
            </div>
            <p style={{ whiteSpace: "pre-wrap" }}>{memo.summary}</p>
            <pre
              style={{
                backgroundColor: "#f8fafc",
                border: "1px solid #e2e8f0",
                borderRadius: 8,
                padding: 12,
                overflowX: "auto",
              }}
            >
              {JSON.stringify(memo.structured_rationale, null, 2)}
            </pre>
          </>
        ) : (
          <p>No memo available.</p>
        )}
      </div>
    </section>
  );
}

function renderCitation(citation: EvidenceCitation) {
  return (
    <div key={citation.id} style={{ borderTop: "1px solid #e2e8f0", paddingTop: 12, marginTop: 12 }}>
      <div>
        <strong>Document ID:</strong> {citation.document}
      </div>
      <div>
        <strong>Section ID:</strong> {citation.section}
      </div>
      <p style={{ whiteSpace: "pre-wrap" }}>{citation.excerpt_text}</p>
    </div>
  );
}

const panelStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 16,
  marginTop: 20,
};