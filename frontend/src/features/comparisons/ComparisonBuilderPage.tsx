import { useMutation, useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { getJson, postJson } from "../../api/client";
import type { ComparisonRun, PaginatedResponse, PolicyDocument } from "../../types/api";

type ComparisonPayload = {
  source_document: number;
  run_type: string;
  target_document_ids: number[];
  config_snapshot: Record<string, unknown>;
};

export default function ComparisonBuilderPage() {
  const [sourceDocumentId, setSourceDocumentId] = useState("");
  const [targetIdsText, setTargetIdsText] = useState("");
  const [runType, setRunType] = useState("policy_vs_control");

  const documentsQuery = useQuery({
    queryKey: ["documents-for-comparison"],
    queryFn: () => getJson<PaginatedResponse<PolicyDocument>>("/api/documents/"),
  });

  const documents = documentsQuery.data?.results ?? [];

  const parsedTargetIds = useMemo(() => {
    return targetIdsText
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)
      .map((value) => Number(value))
      .filter((value) => Number.isInteger(value) && value > 0);
  }, [targetIdsText]);

  const mutation = useMutation({
    mutationFn: (payload: ComparisonPayload) =>
      postJson<ComparisonRun>("/api/comparisons/runs/", payload),
  });

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!sourceDocumentId || parsedTargetIds.length === 0) {
      return;
    }

    mutation.mutate({
      source_document: Number(sourceDocumentId),
      run_type: runType,
      target_document_ids: parsedTargetIds,
      config_snapshot: { launched_from: "frontend" },
    });
  }

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Comparison Builder</h2>
      <p style={{ color: "#475569" }}>
        Launch a version, internal-vs-external, or policy-vs-control comparison run.
      </p>

      <form onSubmit={handleSubmit} style={panelStyle}>
        <div style={fieldStyle}>
          <label htmlFor="source-document">Source Document</label>
          <select
            id="source-document"
            value={sourceDocumentId}
            onChange={(event) => setSourceDocumentId(event.target.value)}
            style={inputStyle}
          >
            <option value="">Select a source document</option>
            {documents.map((document) => (
              <option key={document.id} value={document.id}>
                {document.id} - {document.title} ({document.version_label})
              </option>
            ))}
          </select>
        </div>

        <div style={fieldStyle}>
          <label htmlFor="target-document-ids">Target Document IDs</label>
          <input
            id="target-document-ids"
            type="text"
            value={targetIdsText}
            onChange={(event) => setTargetIdsText(event.target.value)}
            placeholder="Example: 2,3"
            style={inputStyle}
          />
        </div>

        <div style={fieldStyle}>
          <label htmlFor="run-type">Run Type</label>
          <select
            id="run-type"
            value={runType}
            onChange={(event) => setRunType(event.target.value)}
            style={inputStyle}
          >
            <option value="version_diff">version_diff</option>
            <option value="internal_vs_external">internal_vs_external</option>
            <option value="policy_vs_control">policy_vs_control</option>
            <option value="cross_document">cross_document</option>
          </select>
        </div>

        <button type="submit" style={buttonStyle} disabled={mutation.isPending}>
          {mutation.isPending ? "Launching..." : "Launch Comparison Run"}
        </button>

        {mutation.isSuccess ? (
          <div style={{ marginTop: 16 }}>
            Created comparison run #{mutation.data.id} with status {mutation.data.status}.
          </div>
        ) : null}

        {mutation.isError ? (
          <div style={{ marginTop: 16 }}>Failed to create comparison run.</div>
        ) : null}
      </form>
    </section>
  );
}

const panelStyle: React.CSSProperties = {
  backgroundColor: "#ffffff",
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 16,
  display: "grid",
  gap: 16,
};

const fieldStyle: React.CSSProperties = {
  display: "grid",
  gap: 8,
};

const inputStyle: React.CSSProperties = {
  padding: 10,
  border: "1px solid #cbd5e1",
  borderRadius: 8,
};

const buttonStyle: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 8,
  border: "1px solid #0f172a",
  backgroundColor: "#0f172a",
  color: "#ffffff",
  fontWeight: 600,
  cursor: "pointer",
};