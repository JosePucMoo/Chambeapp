import { useState, useEffect } from "react";
import { projectService } from "@/services/project";
import type { ProjectBoard } from "@/interfaces/Project";

export function useProjectBoard(projectId: string | undefined) {
  const [board, setBoard] = useState<ProjectBoard | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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

  return { board, isLoading, error, setBoard };
}
