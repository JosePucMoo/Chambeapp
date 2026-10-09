import type { ProjectMember } from "@/interfaces/Project";
import { projectService } from "@/services/project";
import { useCallback, useEffect, useState } from "react";

export const useProjectMembers = (projectId: string) => {
  const [members, setMembers] = useState<ProjectMember[]>([]);
  const [isLoadingMembers, setIsLoadingMembers] = useState(Boolean(projectId));

  const [prevProjectId, setPrevProjectId] = useState(projectId);
  if (prevProjectId !== projectId) {
    setPrevProjectId(projectId);
    if (projectId) setIsLoadingMembers(true);
  }

  const fetchMembers = useCallback(async () => {
    if (!projectId) return;

    try {
      const response = await projectService.get_project_members(projectId);

      setMembers(response.data);
    } catch {
      setMembers([]);
    } finally {
      setIsLoadingMembers(false);
    }
  }, [projectId]);

  const loadMembers = useCallback(async () => {
    if (!projectId) return;

    setIsLoadingMembers(true);
    await fetchMembers();
  }, [projectId, fetchMembers]);

  useEffect(() => {
    void (async () => {
      await fetchMembers();
    })();
  }, [fetchMembers]);

  return {
    members,
    isLoadingMembers,
    loadMembers,
  };
};
