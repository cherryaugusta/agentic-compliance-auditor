import { createBrowserRouter } from "react-router-dom";

import AppLayout from "./AppLayout";
import AdminPage from "../features/admin/AdminPage";
import ComparisonBuilderPage from "../features/comparisons/ComparisonBuilderPage";
import DocumentDetailPage from "../features/documents/DocumentDetailPage";
import DocumentLibraryPage from "../features/documents/DocumentLibraryPage";
import EvalPage from "../features/evals/EvalPage";
import FindingDetailPage from "../features/findings/FindingDetailPage";
import FindingsDashboardPage from "../features/findings/FindingsDashboardPage";
import LineagePage from "../features/lineage/LineagePage";
import MetricsPage from "../features/metrics/MetricsPage";
import ReviewQueuePage from "../features/review-queue/ReviewQueuePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <DocumentLibraryPage /> },
      { path: "documents/:id", element: <DocumentDetailPage /> },
      { path: "lineage", element: <LineagePage /> },
      { path: "comparisons/new", element: <ComparisonBuilderPage /> },
      { path: "findings", element: <FindingsDashboardPage /> },
      { path: "findings/:id", element: <FindingDetailPage /> },
      { path: "review-queue", element: <ReviewQueuePage /> },
      { path: "metrics", element: <MetricsPage /> },
      { path: "evals", element: <EvalPage /> },
      { path: "admin-tools", element: <AdminPage /> },
    ],
  },
]);