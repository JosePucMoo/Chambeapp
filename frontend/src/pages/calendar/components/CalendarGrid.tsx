import { format } from "date-fns";
import { es } from "date-fns/locale";
import { CalendarDayCell } from "./CalendarDayCell";
import type { CalendarDay, CalendarWeek } from "../utils/calendarGrid";
import type { CalendarTask } from "@/interfaces/Task";

interface CalendarGridProps {
  weeks: CalendarWeek[];
  tasksByDay: Map<string, CalendarTask[]>;
  onDayClick: (day: CalendarDay) => void;
  onOpenDetail: (taskId: string) => void;
  onMarkAsDone: (task: CalendarTask) => void;
}

export const CalendarGrid = ({
  weeks,
  tasksByDay,
  onDayClick,
  onOpenDetail,
  onMarkAsDone,
}: CalendarGridProps) => {
  const weekDays = (weeks[0]?.days ?? []).map((day) => {
    const label = format(day.date, "EEE", { locale: es });
    return {
      key: day.key,
      label: label.charAt(0).toUpperCase() + label.slice(1),
    };
  });

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="min-w-160">
        <div className="grid grid-cols-7 border-b border-slate-200 bg-gray-50/60">
          {weekDays.map((weekDay) => (
            <div
              key={weekDay.key}
              className="border-r border-slate-200 px-2 py-2.5 text-center text-xs font-semibold uppercase text-gray-500 last:border-r-0"
            >
              {weekDay.label}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7">
          {weeks.map((week) =>
            week.days.map((day) => (
              <CalendarDayCell
                key={day.key}
                day={day}
                tasks={tasksByDay.get(day.key) ?? []}
                onDayClick={onDayClick}
                onOpenDetail={onOpenDetail}
                onMarkAsDone={onMarkAsDone}
              />
            )),
          )}
        </div>
      </div>
    </div>
  );
};
