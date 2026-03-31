import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { vi } from "vitest";

import FindingDetailPage from "../src/features/findings/FindingDetailPage";

vi.mock("../src/api/client", () => ({
  getJson: vi.fn((url: string) => {
    if (url.endsWith("/citations/")) {
      return Promise.resolve([
        {
          id: 1,
          conflict_flag: 1,
          document: 1,
          section: 1,
          citation_role: "source",
          excerpt_text: "Escalated complaints must be acknowledged within 10 business days.",
        },
        {
          id: 2,
          conflict_flag: 1,
          document: 2,
          section: 2,
          citation_role: "target",
          excerpt_text: "Escalated complaints must be acknowledged within 5 business days.",
        },
      ]);
    }

    if (url.endsWith("/memo/")) {
      return Promise.resolve({
        id: 1,
        conflict_flag: 1,
        recommended_action: "review",
        summary: "Timeline mismatch: source=10 business days, target=5 business days.",
        structured_rationale: {
          degraded_mode: false,
        },
        confidence: 0.92,
        prompt_version: 1,
      });
    }

    return Promise.resolve({
      id: 1,
      comparison_run: 1,
      source_statement: 1,
      target_statement: 2,
      conflict_type: "timeline_conflict",
      severity: "high",
      status: "open",
      confidence: 0.92,
      requires_review: true,
      reason_summary: "Timeline mismatch: source=10 business days, target=5 business days.",
      rules_triggered: ["timeline_mismatch"],
      model_version: "mock-contradiction-model",
    });
  }),
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
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/findings/1"]}>
        <Routes>
          <Route path="/findings/:id" element={ui} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

test("finding detail renders citations and memo", async () => {
  renderWithProviders(<FindingDetailPage />);

  await waitFor(() => {
    expect(screen.getByText("Finding #1")).toBeInTheDocument();
  });

  expect(screen.getByText(/Source Citations/)).toBeInTheDocument();
  expect(screen.getByText(/Target Citations/)).toBeInTheDocument();
  expect(screen.getByText(/Memo/)).toBeInTheDocument();
  expect(screen.getByText("Export finding packet")).toBeInTheDocument();
  expect(
    screen.getByText("Escalated complaints must be acknowledged within 10 business days."),
  ).toBeInTheDocument();
  expect(
    screen.getByText("Escalated complaints must be acknowledged within 5 business days."),
  ).toBeInTheDocument();
  expect(screen.getByText(/Recommended Action:/)).toBeInTheDocument();
  expect(screen.getAllByText(/Timeline mismatch: source=10 business days, target=5 business days\./)).toHaveLength(2);
});