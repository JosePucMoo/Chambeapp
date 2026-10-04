import { useParams } from "react-router-dom";
import { DragDropProvider, type DragEndEvent } from "@dnd-kit/react";
import { useProjectBoard } from "@/hooks/useProjectBoard";
import { Column } from "./Column";

export function Board() {
  const { projectId } = useParams<{ projectId: string }>();

  const { board, isLoading, error, moveTask } = useProjectBoard(projectId);

  if (isLoading) {
    return (
      <div className="p-8 text-center text-slate-500">Cargando tablero...</div>
    );
  }

  if (error || !board) {
    return (
      <div className="p-8 text-center text-red-500">
        {error || "Tablero no encontrado"}
      </div>
    );
  }

  const handleDragEnd = (event: DragEndEvent) => {
    if (event.canceled) return;

    const taskId = event.operation?.source?.id as string;
    const columnId = event.operation?.target?.id as string;

    moveTask(taskId, columnId);
  };

  return (
    <DragDropProvider onDragEnd={handleDragEnd}>
      <div className="flex gap-10 overflow-x-auto justify-start m-0 flex-1 overflow-y-hidden h-full">
        {board.columns.map((column) => (
          <Column
            key={column.id}
            id={column.id}
            title={column.title}
            tasks={column.tasks}
          ></Column>
        ))}
      </div>
    </DragDropProvider>
  );
}
