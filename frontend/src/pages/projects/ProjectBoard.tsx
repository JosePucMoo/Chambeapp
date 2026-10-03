import { Button } from "@/components/ui/button";
import { Filter, UserPlus } from "lucide-react";
import { Board } from "./components/Board";
import { CreateTaskDialog } from "./components/CreateTaskDialog";
import { useParams } from "react-router-dom";

const ProjectBoard = () => {
  const params = useParams();
  const projectId = params.projectId || "";

  return (
    <div className="flex flex-col h-full shadow-sm overflow-hidden gap-10 w-full mx-auto p-10">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-0">
        <div className="flex items-center gap-3">
          <div>
            <h1 className="text-4xl font-bold text-gray-700">InterActive</h1>
            <p className="text-sm text-gray-500">
              La descripcion de mi proyecto
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <Button
            variant="outline"
            className="text-gray-700 font-medium h-10 border-gray-300"
          >
            <UserPlus className="w-4 h-4 text-gray-500" />
            Invitar
          </Button>
          <Button
            variant="outline"
            className="text-gray-700 font-medium h-10 border-gray-300"
          >
            <Filter className="w-4 h-4 text-gray-500" />
            Filtrar
          </Button>
          <CreateTaskDialog loadTasks={() => {}} projectId={projectId} />
        </div>
      </div>

      <Board />
    </div>
  );
};

export default ProjectBoard;
