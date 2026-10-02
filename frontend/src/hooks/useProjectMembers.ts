import type { ProjectMember } from "@/interfaces/Project";
import { projectService } from "@/services/project";
import { useCallback, useEffect, useState } from "react";

export const useProjectMembers = (projectId: string) => {
  const [members, setMembers] = useState<ProjectMember[]>([]);
  const [isLoadingMembers, setIsLoadingMembers] = useState(false);

  const loadMembers = useCallback(async () => {
    if (!projectId) return;

    setIsLoadingMembers(true);
    try {
      const response = await projectService.get_project_members(projectId);

      setMembers(response.data);
    } catch (error) {
      setMembers([]);
    } finally {
      setIsLoadingMembers(false);
    }
  }, [projectId]);

  useEffect(() => {
    loadMembers();
  }, [loadMembers]);

  return {
    members,
    isLoadingMembers,
    loadMembers,
  };
};
