import { useQuery } from "@tanstack/react-query";

import { getJson } from "../../api/client";

type VersionChainResponse = Record<
  string,
  {
    parent_document_id: number;
    parent_title: string;
    child_document_id: number;
    child_title: string;
    relationship_type: string;
  }[]
>;

export default function LineagePage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["lineage-version-chains"],
    queryFn: () => getJson<VersionChainResponse>("/api/lineage/version-chains/"),
  });

  if (isLoading) {
    return <div>Loading lineage...</div>;
  }

  if (isError) {
    return <div>Failed to load lineage: {String(error)}</div>;
  }

  const chains = Object.entries(data ?? {});

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Version Lineage</h2>
      <p style={{ color: "#475569" }}>
        Parent-child document chains and relationship labels.
      </p>

      <div style={{ display: "grid", gap: 16, marginTop: 20 }}>
        {chains.length === 0 ? (
          <div style={panelStyle}>No version chains available.</div>
        ) : (
          chains.map(([title, links]) => (
            <div key={title} style={panelStyle}>
              <h3 style={{ marginTop: 0 }}>{title}</h3>
              {links.map((link, index) => (
                <div
                  key={`${link.parent_document_id}-${link.child_document_id}-${index}`}
                  style={{ borderTop: "1px solid #e2e8f0", paddingTop: 12, marginTop: 12 }}
                >
                  <div>
                    <strong>Parent:</strong> #{link.parent_document_id} - {link.parent_title}
                  </div>
                  <div>
                    <strong>Child:</strong> #{link.child_document_id} - {link.child_title}
                  </div>
                  <div>
                    <strong>Relationship:</strong> {link.relationship_type}
                  </div>
                </div>
              ))}
            </div>
          ))
        )}
      </div>
    </section>
  );
}

const panelStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 16,
};