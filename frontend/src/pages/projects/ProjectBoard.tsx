import { Button } from "@/components/ui/button";
import { Filter, FolderX, UserPlus } from "lucide-react";
import { Board } from "./components/Board";
import { CreateTaskDialog } from "./components/CreateTaskDialog";
import { useParams } from "react-router-dom";
import { ResourceNotFound } from "../NotFound";
import { useProjectBoard } from "@/hooks/useProjectBoard";

const ProjectBoard = () => {
  const params = useParams();
  const projectId = params.projectId || "";

  const { board, moveTask, addTask, isLoading, error } =
    useProjectBoard(projectId);

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
          <Button
            variant="outline"
            className="text-slate-700 font-medium h-10 border-slate-300"
          >
            <UserPlus className="w-4 h-4 text-slate-500" />
            Invitar
          </Button>
          <Button
            variant="outline"
            className="text-slate-700 font-medium h-10 border-slate-300"
          >
            <Filter className="w-4 h-4 text-slate-500" />
            Filtrar
          </Button>
          <CreateTaskDialog addTask={addTask} projectId={projectId} />
        </div>
      </div>

      <Board board={board} moveTask={moveTask} />
    </div>
  );
};

export default ProjectBoard;
