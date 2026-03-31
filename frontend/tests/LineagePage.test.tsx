import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import LineagePage from "../src/features/lineage/LineagePage";

vi.mock("../src/api/client", () => ({
  getJson: vi.fn().mockResolvedValue({
    "Complaints Escalation Policy v3": [
      {
        parent_document_id: 1,
        parent_title: "Complaints Escalation Policy v3",
        child_document_id: 2,
        child_title: "Complaints Control Standard",
        relationship_type: "aligned_to",
      },
    ],
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
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

test("lineage page renders version chain row", async () => {
  renderWithProviders(<LineagePage />);

  await waitFor(() => {
    expect(screen.getByText("Complaints Escalation Policy v3")).toBeInTheDocument();
  });

  expect(screen.getByText(/Parent:/)).toBeInTheDocument();
  expect(screen.getByText(/Child:/)).toBeInTheDocument();
  expect(screen.getByText("aligned_to")).toBeInTheDocument();
});