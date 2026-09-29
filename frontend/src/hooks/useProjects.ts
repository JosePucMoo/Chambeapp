import { useState, useEffect } from "react";
import { projectService } from "@/services/project";
import type { ProjectDashboardSummary } from "@/interfaces/Project";

export function useProjects(page: number, pageSize: number) {
  const [projects, setProjects] = useState<ProjectDashboardSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  useEffect(() => {
    const loadProjects = async () => {
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
    };

    loadProjects();
  }, [page, pageSize]);

  return { projects, isLoading, totalCount, totalPages };
}
