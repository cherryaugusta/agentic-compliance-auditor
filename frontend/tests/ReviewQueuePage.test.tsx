import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import ReviewQueuePage from "../src/features/review-queue/ReviewQueuePage";

const mockPostJson = vi.fn();

vi.mock("../src/api/client", () => ({
  getJson: vi.fn().mockResolvedValue({
    count: 1,
    next: null,
    previous: null,
    results: [
      {
        id: 1,
        conflict_flag: 1,
        queue_name: "policy-review",
        assigned_to: null,
        status: "unassigned",
        reason_code: "high_severity",
        sla_due_at: "2026-04-02T11:07:12.737961+01:00",
      },
    ],
  }),
  postJson: (...args: unknown[]) => mockPostJson(...args),
}));

function renderWithProviders(ui: React.ReactNode) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

test("review queue renders rows and action buttons", async () => {
  mockPostJson.mockResolvedValue({
    id: 1,
    conflict_flag: 1,
    queue_name: "policy-review",
    assigned_to: null,
    status: "assigned",
    reason_code: "high_severity",
    sla_due_at: "2026-04-02T11:07:12.737961+01:00",
  });

  renderWithProviders(<ReviewQueuePage />);

  await waitFor(() => {
    expect(screen.getByText("Review Task #1")).toBeInTheDocument();
  });

  expect(screen.getByText("Assign")).toBeInTheDocument();
  expect(screen.getByText("Approve")).toBeInTheDocument();
  expect(screen.getByText("Override")).toBeInTheDocument();
  expect(screen.getByText("Dismiss")).toBeInTheDocument();
  expect(screen.getByText("Escalate")).toBeInTheDocument();

  fireEvent.click(screen.getByText("Assign"));

  await waitFor(() => {
    expect(mockPostJson).toHaveBeenCalled();
  });
});