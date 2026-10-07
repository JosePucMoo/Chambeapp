import type { ColumnBoard } from "./Column";
import type { ProjectStatusEnum, RoleEnum } from "./constants/enums";

export interface ProjectDashboardSummary {
  id: string;
  title: string;
  client: string;
  role: RoleEnum;
  deliveryDate: string;
  status: ProjectStatusEnum;
  progressPercentage: number;
}

export interface Project {
  id: string;
  title: string;
  description: string;
  client: string;
  deliveryDate?: Date;
}

export interface CreateProject {
  title: string;
  description: string;
  client: string;
  deliveryDate?: Date;
}

export interface ProjectMember {
  id: string;
  name: string;
  email: string;
  role: string;
}

export interface ProjectBoard {
  projectId: string;
  projectTitle: string;
  columns: ColumnBoard[];
}
