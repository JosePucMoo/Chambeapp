import { useState } from "react";
import { useDroppable } from "@dnd-kit/react";
import { Plus } from "lucide-react";
import { CalendarTaskChip } from "./CalendarTaskChip";
import type { CalendarDay } from "../utils/calendarGrid";
import type { CalendarTask } from "@/interfaces/Task";

const MAX_VISIBLE_TASKS = 4;

interface CalendarDayCellProps {
  day: CalendarDay;
  tasks: CalendarTask[];
  onDayClick: (day: CalendarDay) => void;
  onOpenDetail: (taskId: string) => void;
  onMarkAsDone: (task: CalendarTask) => void;
}

export const CalendarDayCell = ({
  day,
  tasks,
  onDayClick,
  onOpenDetail,
  onMarkAsDone,
}: CalendarDayCellProps) => {
  const [expanded, setExpanded] = useState(false);
  const { ref, isDropTarget } = useDroppable({ id: day.key });

  const visibleTasks = expanded ? tasks : tasks.slice(0, MAX_VISIBLE_TASKS);
  const hiddenCount = tasks.length - visibleTasks.length;

  const handleCreate = (event: React.MouseEvent) => {
    event.stopPropagation();
    onDayClick(day);
  };

  return (
    <div
      ref={ref}
      onClick={() => onDayClick(day)}
      className={`group/day relative flex min-h-28 flex-col gap-1 border-b border-r border-slate-200 p-1.5 transition-colors ${
        isDropTarget ? "bg-blue-50/70 ring-1 ring-inset ring-blue-400" : ""
      } ${day.isToday ? "bg-blue-50/40" : ""} ${
        day.isCurrentMonth ? "bg-white" : "bg-slate-50/60"
      }`}
    >
      <div className="flex h-6 items-center justify-between">
        <span
          className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-medium ${
            day.isToday
              ? "bg-blue-500 text-white"
              : day.isCurrentMonth
                ? "text-slate-700"
                : "text-slate-400"
          }`}
        >
          {day.dayOfMonth}
        </span>

        <button
          type="button"
          aria-label="Crear tarea en este día"
          onClick={handleCreate}
          className="rounded-md p-0.5 text-gray-400 opacity-0 transition hover:bg-white hover:text-blue-600 focus-visible:opacity-100 group-hover/day:opacity-100"
        >
          <Plus className="h-4 w-4" />
        </button>
      </div>

      <div
        className="flex flex-col gap-1"
        onClick={(event) => event.stopPropagation()}
      >
        {visibleTasks.map((task) => (
          <CalendarTaskChip
            key={task.id}
            task={task}
            onOpenDetail={onOpenDetail}
            onMarkAsDone={onMarkAsDone}
          />
        ))}

        {hiddenCount > 0 && (
          <button
            type="button"
            onClick={() => setExpanded(true)}
            className="rounded-md px-1 py-0.5 text-left text-[11px] font-medium text-blue-600 hover:bg-blue-50"
          >
            +{hiddenCount} más
          </button>
        )}
      </div>
    </div>
  );
};
