import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";

import { getJson } from "../../api/client";
import StatusBadge from "../../components/StatusBadge";
import type {
  ControlStatement,
  DocumentLineage,
  DocumentSection,
  PolicyDocument,
} from "../../types/api";

export default function DocumentDetailPage() {
  const params = useParams();
  const id = params.id;

  const documentQuery = useQuery({
    queryKey: ["document", id],
    queryFn: () => getJson<PolicyDocument>(`/api/documents/${id}/`),
    enabled: Boolean(id),
  });

  const sectionsQuery = useQuery({
    queryKey: ["document-sections", id],
    queryFn: () => getJson<DocumentSection[]>(`/api/documents/${id}/sections/`),
    enabled: Boolean(id),
  });

  const statementsQuery = useQuery({
    queryKey: ["document-statements", id],
    queryFn: () => getJson<ControlStatement[]>(`/api/documents/${id}/statements/`),
    enabled: Boolean(id),
  });

  const lineageQuery = useQuery({
    queryKey: ["document-lineage", id],
    queryFn: () => getJson<DocumentLineage[]>(`/api/documents/${id}/lineage/`),
    enabled: Boolean(id),
  });

  if (
    documentQuery.isLoading ||
    sectionsQuery.isLoading ||
    statementsQuery.isLoading ||
    lineageQuery.isLoading
  ) {
    return <div>Loading document detail...</div>;
  }

  if (
    documentQuery.isError ||
    sectionsQuery.isError ||
    statementsQuery.isError ||
    lineageQuery.isError
  ) {
    return <div>Failed to load document detail.</div>;
  }

  const document = documentQuery.data;
  const sections = sectionsQuery.data ?? [];
  const statements = statementsQuery.data ?? [];
  const lineage = lineageQuery.data ?? [];

  if (!document) {
    return <div>Document not found.</div>;
  }

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>{document.title}</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 12,
          marginBottom: 24,
        }}
      >
        <div style={cardStyle}>
          <strong>Type</strong>
          <div>{document.document_type}</div>
        </div>
        <div style={cardStyle}>
          <strong>Version</strong>
          <div>{document.version_label}</div>
        </div>
        <div style={cardStyle}>
          <strong>Effective Date</strong>
          <div>{document.effective_date}</div>
        </div>
        <div style={cardStyle}>
          <strong>Status</strong>
          <div style={{ marginTop: 8 }}>
            <StatusBadge value={document.status} />
          </div>
        </div>
        <div style={cardStyle}>
          <strong>Source</strong>
          <div>{document.source_name}</div>
        </div>
        <div style={cardStyle}>
          <strong>Domain</strong>
          <div>{document.domain_area}</div>
        </div>
      </div>

      <div style={panelStyle}>
        <h3>Sections</h3>
        {sections.length === 0 ? (
          <p>No sections available.</p>
        ) : (
          sections.map((section) => (
            <div key={section.id} style={{ borderTop: "1px solid #e2e8f0", paddingTop: 12, marginTop: 12 }}>
              <strong>
                {section.heading ?? `Section ${section.section_index}`}
              </strong>
              <p style={{ whiteSpace: "pre-wrap" }}>{section.text}</p>
            </div>
          ))
        )}
      </div>

      <div style={panelStyle}>
        <h3>Extracted Statements</h3>
        {statements.length === 0 ? (
          <p>No statements available.</p>
        ) : (
          statements.map((statement) => (
            <div
              key={statement.id}
              style={{ borderTop: "1px solid #e2e8f0", paddingTop: 12, marginTop: 12 }}
            >
              <div>
                <strong>Type:</strong> {statement.statement_type}
              </div>
              <div>
                <strong>Normalized:</strong> {statement.normalized_text}
              </div>
              <div>
                <strong>Raw:</strong> {statement.raw_text}
              </div>
            </div>
          ))
        )}
      </div>

      <div style={panelStyle}>
        <h3>Lineage</h3>
        {lineage.length === 0 ? (
          <p>No lineage links available.</p>
        ) : (
          lineage.map((link) => (
            <div key={link.id} style={{ borderTop: "1px solid #e2e8f0", paddingTop: 12, marginTop: 12 }}>
              <div>
                <strong>Relationship:</strong> {link.relationship_type}
              </div>
              <div>
                <strong>Parent Document ID:</strong> {link.parent_document}
              </div>
              <div>
                <strong>Child Document ID:</strong> {link.child_document}
              </div>
            </div>
          ))
        )}
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

const panelStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 16,
  marginTop: 20,
};