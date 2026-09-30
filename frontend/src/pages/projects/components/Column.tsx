import { useDroppable } from "@dnd-kit/react";
import { TaskCard } from "./TaskCard";
import type { Task } from "@/interfaces/Task";

interface ColumnProps {
  id: string;
  title: string;
  tasks: Task[];
}

export function Column({ id, title, tasks }: ColumnProps) {
  const { ref, isDropTarget } = useDroppable({
    id: id,
  });

  return (
    <div className="w-80 shrink-0 flex flex-col max-h-full bg-slate-50 rounded-xl overflow-hidden shadow-sm">
      <div className="p-4 shrink-0 border-b border-gray-200/70">
        <h3 className="font-semibold text-gray-700">{title}</h3>
      </div>

      <div
        ref={ref}
        className={`flex-1 overflow-y-auto p-6 flex flex-col gap-3 min-h-37.5 transition-colors ${
          isDropTarget ? "bg-blue-50/60" : "bg-transparent"
        }`}
      >
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
}
