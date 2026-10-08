import { useState, useEffect, useCallback } from "react";
import { projectService } from "@/services/project";
import type {
  ProjectDashboardSummary,
  ProjectFilters,
} from "@/interfaces/Project";

export const useProjects = (
  page: number,
  pageSize: number,
  filters?: ProjectFilters,
) => {
  const [projects, setProjects] = useState<ProjectDashboardSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const requestKey = `${page}:${pageSize}:${JSON.stringify(filters ?? {})}`;
  const [prevRequestKey, setPrevRequestKey] = useState(requestKey);

  if (prevRequestKey !== requestKey) {
    setPrevRequestKey(requestKey);
    setIsLoading(true);
  }

  const fetchProjects = useCallback(async () => {
    try {
      const response = await projectService.get_dashboard_projects(
        page,
        pageSize,
        filters,
      );

      setProjects(response.data.data);
      setTotalCount(response.data.totalCount);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error("Error cargando los proyectos", error);
    } finally {
      setIsLoading(false);
    }
  }, [page, pageSize, filters]);

  const loadProjects = useCallback(async () => {
    setIsLoading(true);
    await fetchProjects();
  }, [fetchProjects]);

  useEffect(() => {
    void (async () => {
      await fetchProjects();
    })();
  }, [fetchProjects]);

  return { projects, isLoading, totalCount, totalPages, loadProjects };
};
