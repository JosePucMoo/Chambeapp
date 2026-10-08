import type { ApiResponse } from "@/interfaces/Api";
import apiClient from "./api";
import type { PaginatedResponse } from "@/interfaces/Paginated";
import type {
  CreateProject,
  Project,
  ProjectBoard,
  ProjectDashboardSummary,
  ProjectFilters,
  ProjectMember,
} from "@/interfaces/Project";
import type { TaskFilters } from "@/interfaces/Task";
import type { InviteMemberDTO } from "@/interfaces/Invitation";

export const projectService = {
  get_dashboard_projects: async (
    page: number = 1,
    pageSize: number = 10,
    filters?: ProjectFilters,
  ): Promise<ApiResponse<PaginatedResponse<ProjectDashboardSummary>>> => {
    const params: Record<string, string> = {
      page: String(page),
      page_size: String(pageSize),
    };
    if (filters?.search) params.search = filters.search;
    if (filters?.status) params.status = filters.status;
    if (filters?.role) params.role = filters.role;

    const response = await apiClient.get("/projects/", { params });

    return response.data;
  },

  create: async (project: CreateProject): Promise<ApiResponse<Project>> => {
    const response = await apiClient.post("/projects/", project);
    return response.data;
  },

  get_project_members: async (
    projectId: string,
  ): Promise<ApiResponse<ProjectMember[]>> => {
    const response = await apiClient.get(`/projects/${projectId}/members`);
    return response.data;
  },

  get_project_by_id: async (
    projectId: string,
  ): Promise<ApiResponse<Project>> => {
    const response = await apiClient.get(`/projects/${projectId}`);
    return response.data;
  },

  get_project_board: async (
    projectId: string,
    filters?: TaskFilters,
  ): Promise<ApiResponse<ProjectBoard>> => {
    const params: Record<string, string> = {};
    if (filters?.priority) params.priority = filters.priority;
    if (filters?.columnTitle) params.column_title = filters.columnTitle;
    if (filters?.projectId) params.project_id = filters.projectId;
    if (filters?.search) params.search = filters.search;

    const response = await apiClient.get(`/projects/${projectId}/board`, {
      params,
    });
    return response.data;
  },

  sendInvitation: async (
    project_id: string,
    invitation_member: InviteMemberDTO,
  ): Promise<ApiResponse<null>> => {
    const response = await apiClient.post(
      `/invitations/project/${project_id}`,
      invitation_member,
    );
    return response.data;
  },
};
