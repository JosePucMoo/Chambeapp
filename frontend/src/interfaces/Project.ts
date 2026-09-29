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
