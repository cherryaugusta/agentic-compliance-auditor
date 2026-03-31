import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";

import DocumentLibraryPage from "../src/features/documents/DocumentLibraryPage";

vi.mock("../src/api/client", () => ({
  getJson: vi.fn().mockResolvedValue({
    count: 1,
    next: null,
    previous: null,
    results: [
      {
        id: 1,
        title: "Complaints Escalation Policy v3",
        document_type: "internal_policy",
        source_name: "Internal Policy Office",
        jurisdiction: null,
        domain_area: "complaints",
        owner_team: "Compliance",
        version_label: "v3",
        effective_date: "2026-01-15",
        supersedes_document: null,
        is_external_source: false,
        status: "active",
        storage_path: "demo_data/internal_policies/complaints_escalation_policy_v3.txt",
        sha256_checksum: "checksum",
        content_text: "Escalated complaints must be acknowledged within 10 business days.",
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
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>,
  );
}

test("document list renders seeded row", async () => {
  renderWithProviders(<DocumentLibraryPage />);

  await waitFor(() => {
    expect(screen.getByText("Complaints Escalation Policy v3")).toBeInTheDocument();
  });

  expect(screen.getByText("internal_policy")).toBeInTheDocument();
  expect(screen.getByText("v3")).toBeInTheDocument();
  expect(screen.getByText("2026-01-15")).toBeInTheDocument();
  expect(screen.getByText("active")).toBeInTheDocument();
});