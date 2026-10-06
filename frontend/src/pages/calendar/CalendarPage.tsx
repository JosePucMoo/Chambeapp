import { useEffect, useMemo, useRef, useState } from "react";
import { DragDropProvider, type DragEndEvent } from "@dnd-kit/react";
import { useOutletContext } from "react-router-dom";
import { CalendarHeader } from "./components/CalendarHeader";
import { CalendarGrid } from "./components/CalendarGrid";
import {
  CalendarEmpty,
  CalendarError,
  CalendarSkeleton,
} from "./components/CalendarStates";
import {
  buildCalendarGrid,
  buildVisibleRange,
  groupTasksByDay,
} from "./utils/calendarGrid";
import type { CalendarDay } from "./utils/calendarGrid";
import { useCalendarTasks } from "@/hooks/useCalendarTasks";
import { TaskDetailSheet } from "@/components/task/TaskDetailSheet";
import { CreateTaskDialog } from "@/pages/projects/components/CreateTaskDialog";
import type { LayoutContextType } from "@/interfaces/Context";
import type { TaskFilters } from "@/interfaces/Task";

const EMPTY_FILTERS: TaskFilters = {
  priority: undefined,
  columnTitle: undefined,
  projectId: undefined,
  search: undefined,
};

const CalendarPage = () => {
  const { setPageTitle } = useOutletContext<LayoutContextType>();
  const [cursor, setCursor] = useState(() => new Date());
  const [filters, setFilters] = useState<TaskFilters>(EMPTY_FILTERS);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [isSheetOpen, setIsSheetOpen] = useState(false);
  const [createDay, setCreateDay] = useState<CalendarDay | null>(null);

  useEffect(() => {
    setPageTitle("Calendario");
  }, [setPageTitle]);

  const weeks = useMemo(() => buildCalendarGrid(cursor), [cursor]);
  const visibleRange = useMemo(() => buildVisibleRange(cursor), [cursor]);

  const { tasks, isLoading, error, reload, moveTask, markAsDone } =
    useCalendarTasks(visibleRange.startDate, visibleRange.endDate, filters);

  const tasksByDay = useMemo(() => groupTasksByDay(tasks), [tasks]);

  const lastDragEndAt = useRef(0);

  const wasJustDragging = () => Date.now() - lastDragEndAt.current < 300;

  const handleDragEnd = (event: DragEndEvent) => {
    lastDragEndAt.current = Date.now();

    if (event.canceled || !event.operation?.target) return;

    const taskId = event.operation?.source?.id;
    const nextDueDate = event.operation?.target?.id;
    const task = tasks.find((item) => item.id === taskId);

    if (!task || typeof nextDueDate !== "string") return;

    void moveTask(task, nextDueDate);
  };

  const openTaskSheet = (taskId: string) => {
    if (wasJustDragging()) return;

    setSelectedTaskId(taskId);
    setIsSheetOpen(true);
  };

  const handleDayClick = (day: CalendarDay) => {
    if (wasJustDragging()) return;

    setCreateDay(day);
  };

  return (
    <div className="flex w-full flex-col gap-6 px-4 py-5 sm:px-10">
      <CalendarHeader
        cursor={cursor}
        filters={filters}
        onCursorChange={setCursor}
        onFiltersChange={setFilters}
        onToday={() => setCursor(new Date())}
      />

      {isLoading ? (
        <CalendarSkeleton />
      ) : error ? (
        <CalendarError message={error} onRetry={reload} />
      ) : (
        <>
          {tasks.length === 0 && <CalendarEmpty />}

          <DragDropProvider onDragEnd={handleDragEnd}>
            <CalendarGrid
              weeks={weeks}
              tasksByDay={tasksByDay}
              onDayClick={handleDayClick}
              onOpenDetail={openTaskSheet}
              onMarkAsDone={(task) => void markAsDone(task)}
            />
          </DragDropProvider>
        </>
      )}

      <TaskDetailSheet
        taskId={selectedTaskId}
        open={isSheetOpen}
        onOpenChange={setIsSheetOpen}
        onTaskUpdated={reload}
        onTaskDeleted={reload}
      />

      {createDay && (
        <CreateTaskDialog
          key={createDay.key}
          open
          onOpenChange={(nextOpen) => {
            if (!nextOpen) setCreateDay(null);
          }}
          defaultDueDate={createDay.key}
          onCreated={reload}
        />
      )}
    </div>
  );
};

export default CalendarPage;
