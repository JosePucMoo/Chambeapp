import type { ApiResponse } from "./../interfaces/Api";
import type { CreateTask, Task } from "./../interfaces/Task";
import apiClient from "./api";

export const taskService = {
  create: async (
    task: CreateTask,
    projectId: string,
  ): Promise<ApiResponse<Task>> => {
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
};
