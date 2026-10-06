import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { toast } from "@/components/ui/toast";
import type { CalendarTask, TaskFilters, UpdateTask } from "@/interfaces/Task";
import type { ColumnBoard } from "@/interfaces/Column";
import { taskService } from "@/services/task";
import { projectService } from "@/services/project";
import { parseDateOnly } from "@/utils/date";

interface CalendarState {
  signature: string;
  tasks: CalendarTask[];
  error: string | null;
}

const buildSignature = (
  startDate: string,
  endDate: string,
  filters: TaskFilters,
): string =>
  [
    startDate,
    endDate,
    filters.priority ?? "",
    filters.columnTitle ?? "",
    filters.projectId ?? "",
    filters.search ?? "",
  ].join("|");

const getErrorMessage = (error: unknown, fallback: string): string =>
  error instanceof Error && error.message ? error.message : fallback;

export const useCalendarTasks = (
  startDate: string,
  endDate: string,
  filters: TaskFilters,
) => {
  const [state, setState] = useState<CalendarState | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const boardCache = useRef<Map<string, ColumnBoard[]>>(new Map());

  const signature = useMemo(
    () => buildSignature(startDate, endDate, filters),
    [startDate, endDate, filters],
  );

  useEffect(() => {
    let active = true;

    taskService
      .get_calendar_tasks(startDate, endDate, filters)
      .then((response) => {
        if (!active) return;

        setState({
          signature,
          tasks: response.data,
          error: null,
        });
      })
      .catch((error: unknown) => {
        if (!active) return;

        setState({
          signature,
          tasks: [],
          error: getErrorMessage(error, "No pudimos cargar las tareas."),
        });
      });

    return () => {
      active = false;
    };
  }, [signature, startDate, endDate, filters, refreshKey]);

  const isLoading = !state || state.signature !== signature;
  const tasks = isLoading ? [] : (state?.tasks ?? []);
  const error = isLoading ? null : (state?.error ?? null);

  const reload = useCallback(() => {
    setState(null);
    setRefreshKey((current) => current + 1);
  }, []);

  const patchTask = useCallback(
    (taskId: string, patch: Partial<CalendarTask>) => {
      setState((current) =>
        current
          ? {
              ...current,
              tasks: current.tasks.map((task) =>
                task.id === taskId ? { ...task, ...patch } : task,
              ),
            }
          : current,
      );
    },
    [],
  );

  const moveTask = useCallback(
    async (task: CalendarTask, nextDueDate: string) => {
      if (task.dueDate === nextDueDate) return;

      patchTask(task.id, { dueDate: nextDueDate });

      try {
        const payload: UpdateTask = {
          title: task.title,
          description: task.description,
          priority: task.priority,
          dueDate: parseDateOnly(nextDueDate),
          assigneeId: task.assigneeId,
        };

        await taskService.update(payload, task.id);

        toast.add({
          type: "success",
          title: "Fecha actualizada",
          description: `La tarea "${task.title}" se movio al ${formatDateLabel(nextDueDate)}.`,
        });
      } catch (moveError) {
        patchTask(task.id, { dueDate: task.dueDate });

        toast.add({
          type: "error",
          title: "No pudimos mover la tarea",
          description: getErrorMessage(
            moveError,
            "Ocurrio un error al actualizar la fecha. Intenta de nuevo.",
          ),
        });
      }
    },
    [patchTask],
  );

  const getCompletedColumn = useCallback(
    async (projectId: string): Promise<ColumnBoard | null> => {
      const cached = boardCache.current.get(projectId);

      if (cached) {
        return findCompletedColumn(cached);
      }

      const response = await projectService.get_project_board(projectId);
      const columns = response.data.columns;

      boardCache.current.set(projectId, columns);

      return findCompletedColumn(columns);
    },
    [],
  );

  const markAsDone = useCallback(
    async (task: CalendarTask) => {
      if (task.isCompleted) return;

      let completedColumn: ColumnBoard | null;

      try {
        completedColumn = await getCompletedColumn(task.projectId);
      } catch (boardError) {
        toast.add({
          type: "error",
          title: "No pudimos completar la tarea",
          description: getErrorMessage(
            boardError,
            "No se pudo obtener el estado del proyecto.",
          ),
        });
        return;
      }

      if (!completedColumn) {
        toast.add({
          type: "error",
          title: "No pudimos completar la tarea",
          description: "El proyecto no tiene una columna de terminado.",
        });
        return;
      }

      patchTask(task.id, {
        columnId: completedColumn.id,
        columnTitle: completedColumn.title,
        isCompleted: true,
      });

      try {
        await taskService.updateTaskPosition(task.id, completedColumn.id);

        toast.add({
          type: "success",
          title: "Tarea completada",
          description: `"${task.title}" ahora esta en ${completedColumn.title}.`,
        });

        if (filters.columnTitle) {
          reload();
        }
      } catch (doneError) {
        patchTask(task.id, {
          columnId: task.columnId,
          columnTitle: task.columnTitle,
          isCompleted: task.isCompleted,
        });

        toast.add({
          type: "error",
          title: "No pudimos completar la tarea",
          description: getErrorMessage(
            doneError,
            "Ocurrio un error al actualizar el estado.",
          ),
        });
      }
    },
    [filters.columnTitle, getCompletedColumn, patchTask, reload],
  );

  return {
    tasks,
    isLoading,
    error,
    reload,
    moveTask,
    markAsDone,
  };
};

const findCompletedColumn = (columns: ColumnBoard[]): ColumnBoard | null => {
  if (columns.length === 0) return null;

  return columns.reduce((best, current) =>
    current.position > best.position ? current : best,
  );
};

const formatDateLabel = (value: string): string => {
  const [year, month, day] = value.split("-");

  return `${day}/${month}/${year}`;
};
