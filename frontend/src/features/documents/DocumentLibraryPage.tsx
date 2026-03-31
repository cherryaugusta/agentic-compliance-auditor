import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { getJson } from "../../api/client";
import StatusBadge from "../../components/StatusBadge";
import type { PaginatedResponse, PolicyDocument } from "../../types/api";

export default function DocumentLibraryPage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["documents"],
    queryFn: () => getJson<PaginatedResponse<PolicyDocument>>("/api/documents/"),
  });

  if (isLoading) {
    return <div>Loading documents...</div>;
  }

  if (isError) {
    return <div>Failed to load documents: {String(error)}</div>;
  }

  const documents = data?.results ?? [];

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Document Library</h2>
      <p style={{ color: "#475569" }}>
        Seeded policy, procedure, guidance, and control documents.
      </p>

      <div
        style={{
          marginTop: 20,
          backgroundColor: "#ffffff",
          border: "1px solid #e2e8f0",
          borderRadius: 12,
          overflowX: "auto",
        }}
      >
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f8fafc", textAlign: "left" }}>
              <th style={{ padding: 12 }}>Title</th>
              <th style={{ padding: 12 }}>Type</th>
              <th style={{ padding: 12 }}>Version</th>
              <th style={{ padding: 12 }}>Effective Date</th>
              <th style={{ padding: 12 }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((document) => (
              <tr key={document.id} style={{ borderTop: "1px solid #e2e8f0" }}>
                <td style={{ padding: 12 }}>
                  <Link to={`/documents/${document.id}`}>{document.title}</Link>
                </td>
                <td style={{ padding: 12 }}>{document.document_type}</td>
                <td style={{ padding: 12 }}>{document.version_label}</td>
                <td style={{ padding: 12 }}>{document.effective_date}</td>
                <td style={{ padding: 12 }}>
                  <StatusBadge value={document.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}