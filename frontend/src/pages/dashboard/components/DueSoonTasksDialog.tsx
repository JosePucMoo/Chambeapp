import { AlertCircle, CalendarClock, RefreshCw } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { PRIORITY_CONFIG } from "@/interfaces/constants/taskMappings";
import { formatDate } from "@/utils/dateFormatter";
import type { TaskDashboardSummary } from "@/interfaces/Task";

interface DueSoonTasksDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  totalDueSoon: number;
  tasks: TaskDashboardSummary[];
  isLoading: boolean;
  error: string | null;
  onRetry: () => void;
}

const DueSoonTasksDialog = ({
  open,
  onOpenChange,
  totalDueSoon,
  tasks,
  isLoading,
  error,
  onRetry,
}: DueSoonTasksDialogProps) => (
  <Dialog open={open} onOpenChange={onOpenChange}>
    <DialogContent className="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle className="text-slate-700 text-xl">
          Tareas que vencen pronto
        </DialogTitle>
        <DialogDescription>
          {totalDueSoon === 1
            ? "Tienes 1 tarea sin completar que vence en los próximos 7 días."
            : `Tienes ${totalDueSoon} tareas sin completar que vencen en los próximos 7 días.`}
        </DialogDescription>
      </DialogHeader>

      <div className="max-h-96 overflow-y-auto -mx-1 px-1">
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, index) => (
              <Skeleton key={index} className="h-16 w-full" />
            ))}
          </div>
        ) : error ? (
          <div className="flex flex-col items-center gap-3 py-8 text-center">
            <AlertCircle className="text-rose-500 w-6 h-6" />
            <p className="text-sm text-slate-600">{error}</p>
            <Button variant="outline" size="sm" onClick={onRetry}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Reintentar
            </Button>
          </div>
        ) : tasks.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-10 text-center">
            <div className="p-3 bg-emerald-50 rounded-full">
              <CalendarClock className="text-emerald-500 w-5 h-5" />
            </div>
            <p className="text-sm font-medium text-slate-800">
              Nada vence pronto
            </p>
            <p className="text-sm text-slate-500">
              No tienes tareas pendientes con vencimiento en los próximos 7
              días.
            </p>
          </div>
        ) : (
          <ul className="divide-y divide-slate-100">
            {tasks.map((task) => (
              <li key={task.id} className="py-3 first:pt-0 last:pb-0">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="font-medium text-slate-800 truncate">
                      {task.title}
                    </p>
                    <p className="text-sm text-slate-500 truncate mt-0.5">
                      {task.projectTitle} · {task.columnTitle}
                    </p>
                  </div>
                  <Badge
                    className={`shrink-0 ${PRIORITY_CONFIG[task.priority].colorClass}`}
                  >
                    {PRIORITY_CONFIG[task.priority].label}
                  </Badge>
                </div>

                <p className="flex items-center gap-1.5 text-sm text-slate-600 mt-2">
                  <CalendarClock className="w-3.5 h-3.5 shrink-0" />
                  <span>{formatDate(task.dueDate, "medium")}</span>
                  <span className="text-slate-400">·</span>
                  <span className="text-amber-600 font-medium">
                    {formatDate(task.dueDate, "relative")}
                  </span>
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </DialogContent>
  </Dialog>
);

export default DueSoonTasksDialog;