import { useQuery } from "@tanstack/react-query";

import { getJson } from "../../api/client";
import type { VersionChain } from "../../types/api";

export default function LineagePage() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["lineage-version-chains"],
    queryFn: () => getJson<VersionChain[]>("/api/lineage/version_chains/"),
  });

  if (isLoading) {
    return <div>Loading lineage...</div>;
  }

  if (isError) {
    return <div>Failed to load lineage: {String(error)}</div>;
  }

  const chains = data ?? [];

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
          chains.map((chain, index) => (
            <div key={`${chain.title}-${index}`} style={panelStyle}>
              <h3 style={{ marginTop: 0 }}>{chain.title}</h3>
              {chain.links.map((link, linkIndex) => (
                <div key={linkIndex} style={{ borderTop: "1px solid #e2e8f0", paddingTop: 12, marginTop: 12 }}>
                  <div>
                    <strong>Parent Document ID:</strong> {link.parent_document}
                  </div>
                  <div>
                    <strong>Child Document ID:</strong> {link.child_document}
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