import { format } from "date-fns";
import { es } from "date-fns/locale";
import { CalendarDays, ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TaskFilterPopover } from "@/components/task/TaskFilterPopover";
import type { TaskFilters } from "@/interfaces/Task";
import { addMonths } from "@/utils/date";

interface CalendarHeaderProps {
  cursor: Date;
  filters: TaskFilters;
  onCursorChange: (cursor: Date) => void;
  onFiltersChange: (filters: TaskFilters) => void;
  onToday: () => void;
}

export const CalendarHeader = ({
  cursor,
  filters,
  onCursorChange,
  onFiltersChange,
  onToday,
}: CalendarHeaderProps) => {
  const monthLabel = format(cursor, "MMMM 'de' yyyy", { locale: es });

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
          <CalendarDays className="h-5 w-5" />
        </span>

        <h1 className="text-xl font-semibold text-slate-700 sm:text-2xl first-letter:uppercase">
          {monthLabel}
        </h1>

        <div className="ml-2 flex items-center gap-1">
          <Button
            variant="outline"
            size="icon"
            aria-label="Mes anterior"
            onClick={() => onCursorChange(addMonths(cursor, -1))}
            className="h-9 w-9 text-gray-500"
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            aria-label="Mes siguiente"
            onClick={() => onCursorChange(addMonths(cursor, 1))}
            className="h-9 w-9 text-gray-500"
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>

        <Button
          variant="outline"
          onClick={onToday}
          className="ml-1 h-9 text-gray-600"
        >
          Hoy
        </Button>
      </div>

      <TaskFilterPopover filters={filters} onApply={onFiltersChange} />
    </div>
  );
};
