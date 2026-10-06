import { useState, useEffect, useCallback } from "react";
import type { TaskDashboardSummary, TaskFilters } from "@/interfaces/Task";
import { taskService } from "@/services/task";

export const useTasks = (
  page: number,
  pageSize: number,
  filters?: TaskFilters,
) => {
  const [tasks, setTasks] = useState<TaskDashboardSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const requestKey = `${page}:${pageSize}:${JSON.stringify(filters ?? {})}`;
  const [prevRequestKey, setPrevRequestKey] = useState(requestKey);

  if (prevRequestKey !== requestKey) {
    setPrevRequestKey(requestKey);
    setIsLoading(true);
  }

  const fetchTasks = useCallback(async () => {
    try {
      const response = await taskService.get_dashboard_tasks(
        page,
        pageSize,
        filters,
      );

      setTasks(response.data.data);
      setTotalCount(response.data.totalCount);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error("Error cargando los proyectos", error);
    } finally {
      setIsLoading(false);
    }
  }, [page, pageSize, filters]);

  const loadTasks = useCallback(async () => {
    setIsLoading(true);
    await fetchTasks();
  }, [fetchTasks]);

  useEffect(() => {
    void (async () => {
      await fetchTasks();
    })();
  }, [fetchTasks]);

  return { tasks, isLoading, totalCount, totalPages, loadTasks };
};
