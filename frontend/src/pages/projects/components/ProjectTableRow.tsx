import { Checkbox } from "@/components/ui/checkbox";
import { TableCell, TableRow } from "@/components/ui/table";
import { RoleEnum } from "@/interfaces/constants/enums";
import type { ProjectDashboardSummary } from "@/interfaces/Project";
import { CalendarDays, Crown, MoreHorizontal, User } from "lucide-react";
import { Link } from "react-router-dom";
import ProjectStatusBadge from "./ProjectStatusBadge";
import { Progress, ProgressValue } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/utils/dateFormatter";

interface ProjectTableRowProps {
  project: ProjectDashboardSummary;
  isSelected: boolean;
  onToggleSelect: (id: string) => void;
}

export const ProjectTableRow = ({
  project,
  isSelected,
  onToggleSelect,
}: ProjectTableRowProps) => {
  return (
    <TableRow className="hover:bg-gray-100 border-b-gray-100 last:border-0 group transition-colors cursor-pointer">
      <TableCell className="pl-6">
        <Checkbox
          checked={isSelected}
          onCheckedChange={() => onToggleSelect(project.id)}
          className="border-gray-300 rounded-lg"
        />
      </TableCell>

      <TableCell>
        <Link
          to={`/projects/${project.id}`}
          className="flex items-center gap-3 w-full group/link"
        >
          <div className="w-8 h-8 rounded-md bg-blue-500 flex items-center justify-center text-white font-bold text-sm shadow-sm group-hover/link:ring-2 ring-offset-1 ring-blue-500 transition-all">
            {project.title.charAt(0).toUpperCase()}
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-gray-700 group-hover/link:text-blue-600 transition-colors">
              {project.title}
            </span>
            <span className="text-xs text-gray-500 font-medium">
              {project.client}
            </span>
          </div>
        </Link>
      </TableCell>

      <TableCell>
        <div className="flex items-center gap-2 text-sm font-medium">
          {project.role === RoleEnum.OWNER ? (
            <>
              <Crown className="w-4 h-4 text-amber-500" />
              <span className="text-gray-500">Dueño</span>
            </>
          ) : (
            <>
              <User className="w-4 h-4 text-gray-500" />
              <span className="text-gray-500">Invitado</span>
            </>
          )}
        </div>
      </TableCell>

      <TableCell>
        <div className="flex items-center text-gray-500 font-medium gap-2 text-sm">
          <CalendarDays className="w-4 h-4 text-gray-500" />
          {formatDate(project.deliveryDate)}
        </div>
        <span className="text-xs text-gray-400 pl-6">
          {formatDate(project.deliveryDate, "relative")}
        </span>
      </TableCell>

      <TableCell>
        <ProjectStatusBadge status={project.status} />
      </TableCell>

      <TableCell>
        <div className="flex items-center gap-3">
          <Progress
            value={project.progressPercentage}
            className="w-full max-w-sm"
          >
            <ProgressValue />
          </Progress>
        </div>
      </TableCell>

      <TableCell className="pr-6">
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 text-gray-500 group-hover:opacity-100 transition-opacity"
        >
          <MoreHorizontal className="h-5 w-5" />
        </Button>
      </TableCell>
    </TableRow>
  );
};
