import { useState } from "react";
import { FolderX } from "lucide-react";
import { Board } from "./components/Board";
import { CreateTaskDialog } from "./components/CreateTaskDialog";
import { InviteMemberPopover } from "./components/InviteMemberPopover";
import { useParams } from "react-router-dom";
import { ResourceNotFound } from "../NotFound";
import { useProjectBoard } from "@/hooks/useProjectBoard";
import { useProjectMembers } from "@/hooks/useProjectMembers";
import { useAuth } from "@/hooks/useAuth";
import { TaskDetailSheet } from "@/components/task/TaskDetailSheet";
import { TaskFilterPopover } from "@/components/task/TaskFilterPopover";
import { RoleEnum } from "@/interfaces/constants/enums";
import type { TaskFilters } from "@/interfaces/Task";

const EMPTY_FILTERS: TaskFilters = {
  priority: undefined,
  columnTitle: undefined,
  projectId: undefined,
  search: "",
};

const ProjectBoard = () => {
  const params = useParams();
  const projectId = params.projectId || "";
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [isTaskSheetOpen, setIsTaskSheetOpen] = useState(false);
  const [filters, setFilters] = useState<TaskFilters>(EMPTY_FILTERS);

  const { user } = useAuth();
  const { members } = useProjectMembers(projectId);
  const isOwner = members.some(
    (member) => member.id === user?.id && member.role === RoleEnum.OWNER,
  );

  const { board, moveTask, addTask, isLoading, error, loadBoard } =
    useProjectBoard(projectId, filters);

  const openTaskSheet = (taskId: string) => {
    setSelectedTaskId(taskId);
    setIsTaskSheetOpen(true);
  };

  const refreshBoard = () => loadBoard(false);

  if (isLoading) {
    return (
      <div className="p-10 text-center text-slate-500">
        Cargando proyecto...
      </div>
    );
  }

  if (error || !board) {
    return (
      <ResourceNotFound
        title="Proyecto no encontrado"
        description="El tablero que intentas buscar no existe."
        icon={FolderX}
        backUrl="/projects"
        backText="Volver a mis proyectos"
      />
    );
  }
  return (
    <div className="flex flex-col h-full shadow-sm overflow-hidden gap-10 w-full mx-auto p-10">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-0">
        <div className="flex flex-col items-start gap-4">
          <h1 className="text-3xl font-semibold text-slate-700">
            {board.projectTitle}
          </h1>
        </div>
        <div className="flex items-center gap-3 w-full sm:w-auto">
          {isOwner && <InviteMemberPopover projectId={projectId} />}
          <TaskFilterPopover
            label="Filtrar"
            filters={filters}
            onApply={setFilters}
            showStateField={false}
            showProjectField={false}
          />
          <CreateTaskDialog addTask={addTask} projectId={projectId} />
        </div>
      </div>
      <Board board={board} moveTask={moveTask} onTaskClick={openTaskSheet} />

      <TaskDetailSheet
        taskId={selectedTaskId}
        open={isTaskSheetOpen}
        onOpenChange={setIsTaskSheetOpen}
        onTaskUpdated={refreshBoard}
        onTaskDeleted={refreshBoard}
      />
    </div>
  );
};

export default ProjectBoard;
