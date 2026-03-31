import { createBrowserRouter } from "react-router-dom";
import HomePage from "../pages/HomePage";
import RunsPage from "../pages/RunsPage";
import FindingsPage from "../pages/FindingsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/runs",
    element: <RunsPage />,
  },
  {
    path: "/findings",
    element: <FindingsPage />,
  },
]);