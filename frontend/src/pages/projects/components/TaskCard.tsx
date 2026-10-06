import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardAction,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { TaskPriorityEnum } from "@/interfaces/constants/enums";
import { PRIORITY_CONFIG } from "@/interfaces/constants/taskMappings";
import type { TaskCardSummary } from "@/interfaces/Task";
import { formatDate } from "@/utils/dateFormatter";
import { useDraggable } from "@dnd-kit/react";
import { CalendarDays } from "lucide-react";

interface TaskCardProps {
  task: TaskCardSummary;
  onClick?: (taskId: string) => void;
}

export const TaskCard = ({ task, onClick }: TaskCardProps) => {
  const { ref } = useDraggable({
    id: task.id,
  });

  const priorityConfig = PRIORITY_CONFIG[task.priority as TaskPriorityEnum];

  return (
    <Card
      ref={ref}
      onClick={() => onClick?.(task.id)}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                onClick(task.id);
              }
            }
          : undefined
      }
      className={`mx-auto w-full pt-0 ring-0 ${
        onClick ? "cursor-pointer transition-shadow hover:shadow-md" : ""
      }`}
    >
      <CardAction className="pt-2 pl-2">
        <Badge variant="secondary" className={`${priorityConfig.colorClass}`}>
          {priorityConfig.label}
        </Badge>
      </CardAction>
      <CardHeader className="">
        <CardTitle className="text-md font-medium text-slate-700">
          {task.title}
        </CardTitle>
      </CardHeader>
      <CardFooter className="flex justify-end bg-white py-2">
        <div className="flex items-center text-gray-500 font-medium gap-2 text-sm">
          <CalendarDays className="w-4 h-4" />
          {formatDate(task.dueDate.toString())}
        </div>
      </CardFooter>
    </Card>
  );
};
