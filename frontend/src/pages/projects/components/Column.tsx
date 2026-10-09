import { useDroppable } from "@dnd-kit/react";
import { TaskCard } from "./TaskCard";
import type { TaskCardSummary } from "@/interfaces/Task";

interface ColumnProps {
  id: string;
  title: string;
  tasks: TaskCardSummary[];
  onTaskClick?: (taskId: string) => void;
}

export const Column = ({ id, title, tasks, onTaskClick }: ColumnProps) => {
  const { ref, isDropTarget } = useDroppable({
    id: id,
  });

  return (
    <div className="w-80 shrink-0 flex flex-col max-h-full bg-slate-100 rounded-xl overflow-hidden shadow-sm">
      <div className="p-4 shrink-0 border-b border-slate-200/70 flex justify-between">
        <h3 className="font-semibold text-slate-600">{title}</h3>
        <span className="bg-slate-200 text-slate-600 text-xs px-2 py-1 rounded-full">
          {tasks.length}
        </span>
      </div>

      <div ref={ref} className="h-full">
        {tasks.length == 0 ? (
          <div className="text-sm m-6 text-slate-400 text-center py-4 border-2 border-dashed border-slate-200 rounded-lg">
            Sin tareas
          </div>
        ) : (
          <div
            className={`flex-1 overflow-y-auto p-6 flex flex-col gap-3 min-h-37.5 transition-colors ${
              isDropTarget ? "bg-blue-50/60" : "bg-transparent"
            }`}
          >
            {tasks.map((task) => (
              <TaskCard key={task.id} task={task} onClick={onTaskClick} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
