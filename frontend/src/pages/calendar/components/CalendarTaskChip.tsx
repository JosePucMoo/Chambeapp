import { useState } from "react";
import { useDraggable } from "@dnd-kit/react";
import { CheckCircle2, Eye, MoreHorizontal } from "lucide-react";
import {
  Popover,
  PopoverContent,
  PopoverHeader,
  PopoverTitle,
  PopoverTrigger,
} from "@/components/ui/popover";
import { PRIORITY_CONFIG } from "@/interfaces/constants/taskMappings";
import type { TaskPriorityEnum } from "@/interfaces/constants/enums";
import type { CalendarTask } from "@/interfaces/Task";

interface CalendarTaskChipProps {
  task: CalendarTask;
  onOpenDetail: (taskId: string) => void;
  onMarkAsDone: (task: CalendarTask) => void;
}

const getPriorityDot = (priority: TaskPriorityEnum): string =>
  PRIORITY_CONFIG[priority]?.colorClass
    .split(" ")
    .find((className) => className.startsWith("bg-")) ?? "bg-gray-300";

export const CalendarTaskChip = ({
  task,
  onOpenDetail,
  onMarkAsDone,
}: CalendarTaskChipProps) => {
  const [open, setOpen] = useState(false);
  const { ref } = useDraggable({ id: task.id });

  const handleOpenDetail = () => {
    setOpen(false);
    onOpenDetail(task.id);
  };

  const handleMarkAsDone = () => {
    setOpen(false);
    onMarkAsDone(task);
  };

  return (
    <div className="group/chip relative">
      <div
        ref={ref}
        role="button"
        tabIndex={0}
        onClick={handleOpenDetail}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            handleOpenDetail();
          }
        }}
        className={`flex w-full cursor-grab items-center gap-1.5 rounded-md border border-gray-200 bg-white px-1.5 py-2 text-left shadow-sm transition hover:border-blue-300 hover:shadow-md active:cursor-grabbing ${
          task.isCompleted ? "opacity-70" : ""
        }`}
      >
        <span
          className={`h-2.5 w-1 shrink-0 rounded-full ${getPriorityDot(task.priority)}`}
        />
        <span
          className={`min-w-0 flex-1 truncate text-xs leading-tight text-gray-700 ${
            task.isCompleted ? "line-through" : ""
          }`}
          title={`${task.title} · ${task.projectTitle}`}
        >
          {task.title}
        </span>
      </div>

      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger
          render={
            <button
              type="button"
              aria-label="Acciones de la tarea"
              onPointerDown={(event) => event.stopPropagation()}
              onClick={(event) => event.stopPropagation()}
              className="absolute right-0.5 top-1/2 hidden -translate-y-1/2 rounded-md bg-white/90 p-0.5 text-gray-400 shadow-sm hover:bg-white hover:text-gray-600 group-hover/chip:block"
            />
          }
        >
          <MoreHorizontal className="h-3.5 w-3.5" />
        </PopoverTrigger>

        <PopoverContent align="end" className="w-60 p-0">
          <PopoverHeader className="gap-0.5 px-3 py-2.5">
            <PopoverTitle className="truncate text-sm text-slate-700">
              {task.title}
            </PopoverTitle>
            <p className="truncate text-xs text-slate-500">
              {task.projectTitle} · {task.columnTitle}
            </p>
          </PopoverHeader>

          <div className="flex flex-col gap-0.5 border-t border-slate-200 p-1.5">
            <button
              type="button"
              onClick={handleOpenDetail}
              className="flex items-center gap-2 rounded-md px-2.5 py-2 text-sm text-gray-700 hover:bg-gray-50"
            >
              <Eye className="h-4 w-4 text-gray-400" />
              Ver detalle
            </button>

            {!task.isCompleted && (
              <button
                type="button"
                onClick={handleMarkAsDone}
                className="flex items-center gap-2 rounded-md px-2.5 py-2 text-sm text-emerald-700 hover:bg-emerald-50"
              >
                <CheckCircle2 className="h-4 w-4" />
                Marcar como completada
              </button>
            )}
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
};
