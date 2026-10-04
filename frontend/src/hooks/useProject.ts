// hooks/useProject.ts
import { useState, useEffect } from "react";
import { projectService } from "@/services/project";
import type { Project } from "@/interfaces/Project";

export const useProject = (projectId: string) => {
  const [project, setProject] = useState<Project>();
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorStatus, setErrorStatus] = useState<string | null>(null);

  useEffect(() => {
    if (!projectId) {
      setErrorStatus("404");
      setIsLoading(false);
      return;
    }

    const loadProject = async () => {
      setIsLoading(true);
      setErrorStatus(null);

      try {
        const response = await projectService.get_project_by_id(projectId);
        setProject(response.data);
      } catch (error: any) {
        const status = error?.response?.status?.toString() || "404";
        setErrorStatus(status);
      } finally {
        setIsLoading(false);
      }
    };

    loadProject();
  }, [projectId]);

  return { project, isLoading, errorStatus };
};
