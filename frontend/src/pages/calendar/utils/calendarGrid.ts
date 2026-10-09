import {
  eachDayOfInterval,
  endOfMonth,
  endOfWeek,
  startOfMonth,
  startOfWeek,
} from "date-fns";
import { dateKey, isSameMonth, isToday, parseDateOnly } from "@/utils/date";

export interface CalendarDay {
  date: Date;
  key: string;
  dayOfMonth: number;
  isCurrentMonth: boolean;
  isToday: boolean;
}

export interface CalendarWeek {
  key: string;
  days: CalendarDay[];
}

export const buildCalendarGrid = (cursor: Date): CalendarWeek[] => {
  const firstWeek = startOfWeek(startOfMonth(cursor), { weekStartsOn: 1 });
  const lastWeek = endOfWeek(endOfMonth(cursor), { weekStartsOn: 1 });

  const days = eachDayOfInterval({ start: firstWeek, end: lastWeek }).map(
    (date) => ({
      date,
      key: dateKey(date),
      dayOfMonth: date.getDate(),
      isCurrentMonth: isSameMonth(date, cursor),
      isToday: isToday(date),
    }),
  );

  const weeks: CalendarWeek[] = [];

  for (let index = 0; index < days.length; index += 7) {
    const slice = days.slice(index, index + 7);
    weeks.push({
      key: slice[0]?.key ?? String(index),
      days: slice,
    });
  }

  return weeks;
};

export const buildVisibleRange = (
  cursor: Date,
): { startDate: string; endDate: string } => {
  const firstWeek = startOfWeek(startOfMonth(cursor), { weekStartsOn: 1 });
  const lastWeek = endOfWeek(endOfMonth(cursor), { weekStartsOn: 1 });

  return {
    startDate: dateKey(firstWeek),
    endDate: dateKey(lastWeek),
  };
};

export const groupTasksByDay = <T extends { dueDate: string }>(
  tasks: T[],
): Map<string, T[]> => {
  const grouped = new Map<string, T[]>();

  tasks.forEach((task) => {
    const key = dateKey(task.dueDate);
    const bucket = grouped.get(key);

    if (bucket) {
      bucket.push(task);
    } else {
      grouped.set(key, [task]);
    }
  });

  return grouped;
};

export { parseDateOnly };
