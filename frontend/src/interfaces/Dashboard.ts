import type { ProjectStatusEnum } from "./constants/enums";

export interface ProjectStatusCount {
  status: ProjectStatusEnum;
  total: number;
}

export interface WeeklyPerformance {
  name: string;
  completed: number;
  created: number;
}

export interface DashboardMetrics {
  totalProjects: number;
  projectsByStatus: ProjectStatusCount[];
  totalTasks: number;
  completedTasks: number;
  tasksDueSoon: number;
  weeklyPerformance: WeeklyPerformance[];
}
