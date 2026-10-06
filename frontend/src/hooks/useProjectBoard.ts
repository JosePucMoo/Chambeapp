import { useState, useEffect, useCallback } from "react";
import { projectService } from "@/services/project";
import type { ProjectBoard } from "@/interfaces/Project";
import type { TaskCardSummary } from "@/interfaces/Task";
import { taskService } from "@/services/task";

export const useProjectBoard = (projectId: string | undefined) => {
  const [board, setBoard] = useState<ProjectBoard | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const addTask = (newTask: TaskCardSummary) => {
    setBoard((prevBoard) => {
      if (!prevBoard) return prevBoard;

      const newBoard = { ...prevBoard, columns: [...prevBoard.columns] };

      const targetColumnIndex = newBoard.columns.findIndex(
        (c) => c.id === newTask.columnId,
      );

      if (targetColumnIndex !== -1) {
        newBoard.columns[targetColumnIndex] = {
          ...newBoard.columns[targetColumnIndex],
          tasks: [...newBoard.columns[targetColumnIndex].tasks, newTask],
        };
      } else {
        if (newBoard.columns.length > 0) {
          newBoard.columns[0] = {
            ...newBoard.columns[0],
            tasks: [
              ...newBoard.columns[0].tasks,
              { ...newTask, columnId: newBoard.columns[0].id },
            ],
          };
        }
      }

      return newBoard;
    });
  };

  const [prevProjectId, setPrevProjectId] = useState(projectId);
  if (prevProjectId !== projectId) {
    setPrevProjectId(projectId);
    if (projectId) {
      setIsLoading(true);
      setError(null);
    }
  }

  const fetchBoard = useCallback(async () => {
    if (!projectId) return;

    try {
      const response = await projectService.get_project_board(projectId);
      setBoard(response.data);
    } catch {
      setError("No se pudo cargar el tablero del proyecto.");
    } finally {
      setIsLoading(false);
    }
  }, [projectId]);

  const loadBoard = useCallback(
    async (showLoader = true) => {
      if (!projectId) return;

      if (showLoader) setIsLoading(true);
      setError(null);
      await fetchBoard();
    },
    [projectId, fetchBoard],
  );

  useEffect(() => {
    void (async () => {
      await fetchBoard();
    })();
  }, [fetchBoard]);

  const moveTask = async (taskId: string, targetColumnId: string) => {
    setBoard((prevBoard) => {
      if (!prevBoard) return prevBoard;

      const newBoard = { ...prevBoard, columns: [...prevBoard.columns] };
      let taskToMove: TaskCardSummary | null = null;

      newBoard.columns.forEach((col, index) => {
        if (col.id == targetColumnId) return newBoard;
        const taskIndex = col.tasks.findIndex((t) => t.id === taskId);
        if (taskIndex !== -1) {
          taskToMove = col.tasks[taskIndex];
          newBoard.columns[index] = {
            ...col,
            tasks: col.tasks.filter((t) => t.id !== taskId),
          };
        }
      });

      if (taskToMove) {
        const targetColumnIndex = newBoard.columns.findIndex(
          (c) => c.id === targetColumnId,
        );
        if (targetColumnIndex !== -1) {
          const task = taskToMove as TaskCardSummary;
          newBoard.columns[targetColumnIndex] = {
            ...newBoard.columns[targetColumnIndex],
            tasks: [...newBoard.columns[targetColumnIndex].tasks, { ...task }],
          };
        }
      }

      return newBoard;
    });

    try {
      await taskService.updateTaskPosition(taskId, targetColumnId);
    } catch {
      return;
    }
  };

  return { board, isLoading, error, setBoard, moveTask, addTask, loadBoard };
};
