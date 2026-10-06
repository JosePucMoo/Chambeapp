import { useState, useEffect, useCallback } from "react";
import type { DashboardMetrics } from "@/interfaces/Dashboard";
import type { TaskDashboardSummary } from "@/interfaces/Task";
import { dashboardService } from "@/services/dashboard";

const EMPTY_METRICS: DashboardMetrics = {
  totalProjects: 0,
  projectsByStatus: [],
  totalTasks: 0,
  completedTasks: 0,
  tasksDueSoon: 0,
  weeklyPerformance: [],
};

export const useDashboard = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics>(EMPTY_METRICS);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = useCallback(async () => {
    try {
      const response = await dashboardService.get_metrics();

      setMetrics(response.data);
      setError(null);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "No pudimos cargar las métricas del dashboard.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  const loadMetrics = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    await fetchMetrics();
  }, [fetchMetrics]);

  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  const isEmpty = metrics.totalTasks === 0 && metrics.totalProjects === 0;

  return { metrics, isLoading, error, isEmpty, loadMetrics };
};

export const useDueSoonTasks = () => {
  const [tasks, setTasks] = useState<TaskDashboardSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await dashboardService.get_due_soon_tasks();

      setTasks(response.data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "No pudimos cargar las tareas que vencen pronto.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { tasks, isLoading, error, loadTasks };
};
