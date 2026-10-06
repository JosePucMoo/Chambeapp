import { DragDropProvider, type DragEndEvent } from "@dnd-kit/react";
import { Column } from "./Column";
import type { ProjectBoard } from "@/interfaces/Project";

interface BoardProps {
  board: ProjectBoard;
  moveTask: (taskId: string, columnId: string) => void;
  onTaskClick?: (taskId: string) => void;
}

export function Board({ board, moveTask, onTaskClick }: BoardProps) {
  const handleDragEnd = (event: DragEndEvent) => {
    if (event.canceled || !event.operation?.target) return;

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
            onTaskClick={onTaskClick}
          ></Column>
        ))}
      </div>
    </DragDropProvider>
  );
}
