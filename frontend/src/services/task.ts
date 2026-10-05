import type { PaginatedResponse } from "@/interfaces/Paginated";
import type { ApiResponse } from "./../interfaces/Api";
import type {
  CreateTask,
  Task,
  TaskCardSummary,
  TaskDashboardSummary,
} from "./../interfaces/Task";
import apiClient from "./api";

export const taskService = {
  create: async (
    task: CreateTask,
    projectId: string,
  ): Promise<ApiResponse<TaskCardSummary>> => {
    const response = await apiClient.post(`/tasks/${projectId}`, task);
    return response.data;
  },

  updateTaskPosition: async (
    taskId: string,
    columnId: string,
  ): Promise<ApiResponse<Task>> => {
    const response = await apiClient.patch(`/tasks/${taskId}/move`, {
      columnId,
    });
    return response.data;
  },

  get_dashboard_tasks: async (
    page: number = 1,
    pageSize: number = 10,
  ): Promise<ApiResponse<PaginatedResponse<TaskDashboardSummary>>> => {
    const response = await apiClient.get("/tasks/", {
      params: {
        page: page,
        page_size: pageSize,
      },
    });

    return response.data;
  },
};
