import { useState, useEffect, useCallback } from "react";
import type { TaskDashboardSummary } from "@/interfaces/Task";
import { taskService } from "@/services/task";

export const useTasks = (page: number, pageSize: number) => {
  const [tasks, setTasks] = useState<TaskDashboardSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const loadTasks = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await taskService.get_dashboard_tasks(page, pageSize);

      setTasks(response.data.data);
      setTotalCount(response.data.totalCount);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error("Error cargando los proyectos", error);
    } finally {
      setIsLoading(false);
    }
  }, [page, pageSize]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  return { tasks, isLoading, totalCount, totalPages, loadTasks };
};
