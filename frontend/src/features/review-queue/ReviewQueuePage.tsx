import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { getJson, postJson } from "../../api/client";
import StatusBadge from "../../components/StatusBadge";
import type { PaginatedResponse, ReviewTask } from "../../types/api";

export default function ReviewQueuePage() {
  const queryClient = useQueryClient();

  const tasksQuery = useQuery({
    queryKey: ["review-tasks"],
    queryFn: () => getJson<PaginatedResponse<ReviewTask>>("/api/review-tasks/"),
  });

  const actionMutation = useMutation({
    mutationFn: ({ taskId, action, payload }: { taskId: number; action: string; payload: object }) =>
      postJson<ReviewTask>(`/api/review-tasks/${taskId}/${action}/`, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["review-tasks"] });
    },
  });

  if (tasksQuery.isLoading) {
    return <div>Loading review queue...</div>;
  }

  if (tasksQuery.isError) {
    return <div>Failed to load review queue.</div>;
  }

  const tasks = tasksQuery.data?.results ?? [];

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Review Queue</h2>
      <p style={{ color: "#475569" }}>
        Review-required findings and reviewer actions.
      </p>

      <div style={{ display: "grid", gap: 16, marginTop: 20 }}>
        {tasks.map((task) => (
          <div key={task.id} style={panelStyle}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                gap: 12,
                flexWrap: "wrap",
              }}
            >
              <div>
                <h3 style={{ margin: 0 }}>Review Task #{task.id}</h3>
                <p style={{ margin: "8px 0 0 0" }}>
                  Conflict Flag #{task.conflict_flag}
                </p>
              </div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <StatusBadge value={task.status} />
                <StatusBadge value={task.reason_code} />
              </div>
            </div>

            <div style={{ marginTop: 12 }}>
              <strong>Queue:</strong> {task.queue_name}
            </div>
            <div style={{ marginTop: 8 }}>
              <strong>SLA Due:</strong> {task.sla_due_at}
            </div>

            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 16 }}>
              <button
                type="button"
                style={buttonStyle}
                onClick={() =>
                  actionMutation.mutate({
                    taskId: task.id,
                    action: "assign",
                    payload: { username: "reviewer1" },
                  })
                }
              >
                Assign
              </button>
              <button
                type="button"
                style={buttonStyle}
                onClick={() =>
                  actionMutation.mutate({
                    taskId: task.id,
                    action: "approve",
                    payload: { comment: "Approved from frontend." },
                  })
                }
              >
                Approve
              </button>
              <button
                type="button"
                style={buttonStyle}
                onClick={() =>
                  actionMutation.mutate({
                    taskId: task.id,
                    action: "dismiss",
                    payload: { comment: "Dismissed from frontend." },
                  })
                }
              >
                Dismiss
              </button>
              <button
                type="button"
                style={buttonStyle}
                onClick={() =>
                  actionMutation.mutate({
                    taskId: task.id,
                    action: "escalate",
                    payload: { comment: "Escalated from frontend." },
                  })
                }
              >
                Escalate
              </button>
            </div>
          </div>
        ))}
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

const buttonStyle: React.CSSProperties = {
  padding: "8px 12px",
  borderRadius: 8,
  border: "1px solid #0f172a",
  backgroundColor: "#ffffff",
  color: "#0f172a",
  fontWeight: 600,
  cursor: "pointer",
};