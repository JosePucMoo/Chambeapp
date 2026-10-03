import type { ApiResponse } from "./../interfaces/Api";
import type { CreateTask, Task } from "./../interfaces/Task";
import apiClient from "./api";

export const taskService = {
  create: async (
    task: CreateTask,
    projectId: string,
  ): Promise<ApiResponse<Task>> => {
    console.log(task);

    const response = await apiClient.post(`/tasks/${projectId}`, task);
    return response.data;
  },
};
