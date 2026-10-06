import type { PaginatedResponse } from "@/interfaces/Paginated";
import type { ApiResponse } from "./../interfaces/Api";
import type {
  CalendarTask,
  CreateTask,
  Task,
  TaskCardSummary,
  TaskDashboardSummary,
  TaskDetail,
  TaskFilters,
  UpdateTask,
} from "./../interfaces/Task";
import { toDateString } from "@/utils/date";
import apiClient from "./api";

export const taskService = {
  create: async (
    task: CreateTask,
    projectId: string,
  ): Promise<ApiResponse<TaskCardSummary>> => {
    const response = await apiClient.post(`/tasks/${projectId}`, {
      ...task,
      dueDate: toDateString(task.dueDate),
    });
    return response.data;
  },

  get_by_id: async (taskId: string): Promise<ApiResponse<TaskDetail>> => {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return response.data;
  },

  update: async (
    task: UpdateTask,
    taskId: string,
  ): Promise<ApiResponse<Task>> => {
    const response = await apiClient.put(`/tasks/${taskId}`, {
      ...task,
      dueDate: toDateString(task.dueDate),
    });
    return response.data;
  },

  delete: async (taskId: string): Promise<ApiResponse<null>> => {
    const response = await apiClient.delete(`/tasks/${taskId}`);
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

  delete_many: async (taskIds: string[]): Promise<ApiResponse<string[]>> => {
    const response = await apiClient.delete("/tasks/", {
      data: { taskIds },
    });
    return response.data;
  },

  get_dashboard_tasks: async (
    page: number = 1,
    pageSize: number = 10,
    filters?: TaskFilters,
  ): Promise<ApiResponse<PaginatedResponse<TaskDashboardSummary>>> => {
    const response = await apiClient.get("/tasks/", {
      params: {
        page: page,
        page_size: pageSize,
        priority: filters?.priority,
        column_title: filters?.columnTitle,
        project_id: filters?.projectId,
        search: filters?.search,
      },
    });

    return response.data;
  },

  get_calendar_tasks: async (
    startDate: string,
    endDate: string,
    filters?: TaskFilters,
  ): Promise<ApiResponse<CalendarTask[]>> => {
    const response = await apiClient.get("/tasks/calendar", {
      params: {
        start_date: startDate,
        end_date: endDate,
        priority: filters?.priority,
        column_title: filters?.columnTitle,
        project_id: filters?.projectId,
        search: filters?.search,
      },
    });

    return response.data;
  },
};
