import type { ApiResponse } from "@/interfaces/Api";
import apiClient from "./api";
import type { PaginatedResponse } from "@/interfaces/Paginated";
import type {
  CreateProject,
  Project,
  ProjectDashboardSummary,
} from "@/interfaces/Project";

export const projectService = {
  get_dashboard_projects: async (
    page: number = 1,
    pageSize: number = 10,
  ): Promise<ApiResponse<PaginatedResponse<ProjectDashboardSummary>>> => {
    const response = await apiClient.get("/projects/", {
      params: {
        page: page,
        page_size: pageSize,
      },
    });

    return response.data;
  },

  create: async (project: CreateProject): Promise<ApiResponse<Project>> => {
    const response = await apiClient.post("/projects/", project);
    return response.data;
  },
};
