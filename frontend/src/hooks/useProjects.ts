import { useState, useEffect, useCallback } from "react";
import { projectService } from "@/services/project";
import type { ProjectDashboardSummary } from "@/interfaces/Project";

export const useProjects = (page: number, pageSize: number) => {
  const [projects, setProjects] = useState<ProjectDashboardSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const loadProjects = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await projectService.get_dashboard_projects(
        page,
        pageSize,
      );

      setProjects(response.data.data);
      setTotalCount(response.data.totalCount);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error("Error cargando los proyectos", error);
    } finally {
      setIsLoading(false);
    }
  }, [page, pageSize]);

  useEffect(() => {
    loadProjects();
  }, [loadProjects]);

  return { projects, isLoading, totalCount, totalPages, loadProjects };
};
