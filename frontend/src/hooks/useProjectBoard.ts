import { useState, useEffect } from "react";
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

  useEffect(() => {
    if (!projectId) return;

    const loadBoard = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await projectService.get_project_board(projectId);
        setBoard(response.data);
      } catch (error: any) {
        setError("No se pudo cargar el tablero del proyecto.");
      } finally {
        setIsLoading(false);
      }
    };

    loadBoard();
  }, [projectId]);

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
    } catch (error) {
      return;
    }
  };

  return { board, isLoading, error, setBoard, moveTask, addTask };
};
