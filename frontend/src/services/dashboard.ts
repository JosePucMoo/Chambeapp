import type { ApiResponse } from "@/interfaces/Api";
import type { DashboardMetrics } from "@/interfaces/Dashboard";
import type { TaskDashboardSummary } from "@/interfaces/Task";
import apiClient from "./api";

export const dashboardService = {
  get_metrics: async (): Promise<ApiResponse<DashboardMetrics>> => {
    const response = await apiClient.get("/dashboard/");

    return response.data;
  },

  get_due_soon_tasks: async (): Promise<
    ApiResponse<TaskDashboardSummary[]>
  > => {
    const response = await apiClient.get("/dashboard/tasks/due-soon");

    return response.data;
  },
};
