import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { TableCell, TableRow } from "@/components/ui/table";
import {
  COLUMN_STATE_CONFIG,
  PRIORITY_CONFIG,
} from "@/interfaces/constants/taskMappings";
import {
  ColumnDefaultEnum,
  TaskPriorityEnum,
} from "@/interfaces/constants/enums";
import type { TaskDashboardSummary } from "@/interfaces/Task";
import { CalendarDays } from "lucide-react";
import { formatDate } from "@/utils/dateFormatter";

interface TaskTableRowProps {
  task: TaskDashboardSummary;
  isSelected: boolean;
  onToggleSelect: (id: string) => void;
  onOpenTaskSheet: (taskId: string) => void;
}

export const TaskTableRow = ({
  task,
  isSelected,
  onToggleSelect,
  onOpenTaskSheet,
}: TaskTableRowProps) => {
  return (
    <TableRow
      onClick={() => onOpenTaskSheet(task.id)}
      className="hover:bg-gray-100 border-b-gray-100 last:border-0 group cursor-pointer transition-colors"
    >
      <TableCell className="pl-6" onClick={(event) => event.stopPropagation()}>
        <Checkbox
          checked={isSelected}
          onCheckedChange={() => onToggleSelect(task.id)}
          className="border-gray-300 rounded-lg"
        />
      </TableCell>

      <TableCell className="font-medium text-gray-900">{task.title}</TableCell>

      <TableCell>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded bg-blue-500 flex items-center justify-center text-white text-[10px] font-bold">
            {task.projectTitle.charAt(0)}
          </div>
          <span className="text-gray-600">{task.projectTitle}</span>
        </div>
      </TableCell>

      <TableCell>
        <div className="flex items-center text-gray-600 font-medium gap-2 text-sm">
          <CalendarDays className="w-4 h-4 text-gray-400" />
          {formatDate(task.dueDate)}
        </div>
        <span className="text-xs text-gray-400 pl-6">
          {formatDate(task.dueDate, "relative")}
        </span>
      </TableCell>

      <TableCell>
        <Badge
          variant="secondary"
          className={
            PRIORITY_CONFIG[task.priority as TaskPriorityEnum].colorClass
          }
        >
          {PRIORITY_CONFIG[task.priority as TaskPriorityEnum].label}
        </Badge>
      </TableCell>

      <TableCell>
        <Badge
          className={
            COLUMN_STATE_CONFIG[task.columnTitle as ColumnDefaultEnum]
              .colorClass
          }
        >
          {COLUMN_STATE_CONFIG[task.columnTitle as ColumnDefaultEnum].label}
        </Badge>
      </TableCell>
    </TableRow>
  );
};
