import { AlertCircle, CalendarX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

export const CalendarSkeleton = () => {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center gap-2 border-b border-slate-200 bg-gray-50/60 px-4 py-3">
        {Array.from({ length: 7 }).map((_, index) => (
          <Skeleton key={index} className="h-4 flex-1" />
        ))}
      </div>

      <div className="grid grid-cols-7">
        {Array.from({ length: 42 }).map((_, index) => (
          <div
            key={index}
            className="flex min-h-28 flex-col gap-1.5 border-b border-r border-slate-200 p-1.5 last:border-r-0"
          >
            <Skeleton className="h-5 w-5 rounded-full" />
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-6 w-4/5" />
          </div>
        ))}
      </div>
    </div>
  );
};

interface CalendarErrorProps {
  message: string;
  onRetry: () => void;
}

export const CalendarError = ({ message, onRetry }: CalendarErrorProps) => {
  return (
    <div className="flex flex-col items-center justify-center gap-4 rounded-xl border border-rose-100 bg-white px-6 py-14 text-center shadow-sm">
      <span className="flex h-12 w-12 items-center justify-center rounded-full bg-rose-50">
        <AlertCircle className="h-6 w-6 text-rose-500" />
      </span>

      <div className="space-y-1">
        <p className="text-base font-medium text-slate-700">
          No pudimos cargar las tareas.
        </p>
        <p className="text-sm text-slate-500">{message}</p>
      </div>

      <Button variant="outline" onClick={onRetry} className="text-gray-700">
        Reintentar
      </Button>
    </div>
  );
};

export const CalendarEmpty = () => {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-slate-300 bg-white px-6 py-10 text-center">
      <span className="flex h-11 w-11 items-center justify-center rounded-full bg-slate-100">
        <CalendarX className="h-5 w-5 text-slate-400" />
      </span>
      <p className="text-sm font-medium text-slate-600">
        No hay tareas programadas para este periodo.
      </p>
      <p className="text-xs text-slate-400">
        Haz clic en un día para crear una tarea.
      </p>
    </div>
  );
};
