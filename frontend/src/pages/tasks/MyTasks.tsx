import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Calendar, CalendarDays, LayoutList, Trash2 } from "lucide-react";
import { Link, useOutletContext } from "react-router-dom";
import type { LayoutContextType } from "@/interfaces/Context";
import {
  COLUMN_STATE_CONFIG,
  PRIORITY_CONFIG,
} from "@/interfaces/constants/taskMappings";
import {
  ColumnDefaultEnum,
  TaskPriorityEnum,
} from "@/interfaces/constants/enums";
import type { TaskFilters } from "@/interfaces/Task";
import { useTasks } from "@/hooks/useTasks";
import { taskService } from "@/services/task";
import { formatDate } from "@/utils/dateFormatter";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { TaskDetailSheet } from "@/components/task/TaskDetailSheet";
import { TaskFilterPopover } from "@/components/task/TaskFilterPopover";
import { toast } from "@/components/ui/toast";

const EMPTY_FILTERS: TaskFilters = {
  priority: undefined,
  columnTitle: undefined,
  projectId: undefined,
  search: undefined,
};

const MyTasks = () => {
  const [selectedTasks, setSelectedTasks] = useState<string[]>([]);
  const { setPageTitle } = useOutletContext<LayoutContextType>();
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [filters, setFilters] = useState<TaskFilters>(EMPTY_FILTERS);
  const [isBulkDeleteDialogOpen, setIsBulkDeleteDialogOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const memoizedFilters = useMemo(
    () => ({
      priority: filters.priority,
      columnTitle: filters.columnTitle,
      projectId: filters.projectId,
      search: filters.search,
    }),
    [filters],
  );

  const { tasks, totalCount, totalPages, loadTasks } = useTasks(
    currentPage,
    itemsPerPage,
    memoizedFilters,
  );
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [isTaskSheetOpen, setIsTaskSheetOpen] = useState(false);

  const openTaskSheet = (taskId: string) => {
    setSelectedTaskId(taskId);
    setIsTaskSheetOpen(true);
  };

  useEffect(() => {
    setPageTitle("Mis tareas");
  }, [setPageTitle]);

  const toggleSelectAll = () => {
    if (selectedTasks.length === tasks.length) {
      setSelectedTasks([]);
    } else {
      setSelectedTasks(tasks.map((t) => t.id));
    }
  };

  const toggleSelectTask = (id: string) => {
    if (selectedTasks.includes(id)) {
      setSelectedTasks(selectedTasks.filter((taskId) => taskId !== id));
    } else {
      setSelectedTasks([...selectedTasks, id]);
    }
  };

  const handleApplyFilters = (newFilters: TaskFilters) => {
    setFilters(newFilters);
    setCurrentPage(1);
    setSelectedTasks([]);
  };

  const handlePageChange = (page: number, e: React.MouseEvent) => {
    e.preventDefault();
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
      setSelectedTasks([]);
    }
  };

  const handleItemsPerPageChange = (value: string | null) => {
    if (!value) return;
    setItemsPerPage(Number(value));
    setCurrentPage(1);
    setSelectedTasks([]);
  };

  const handleBulkDelete = async () => {
    setIsDeleting(true);
    try {
      const response = await taskService.delete_many(selectedTasks);
      const deletedCount = response.data.length;

      toast.add({
        type: "success",
        title:
          deletedCount === 1
            ? "Tarea eliminada"
            : `${deletedCount} tareas eliminadas`,
        description: "Las tareas se eliminaron correctamente.",
      });

      setSelectedTasks([]);
      setIsBulkDeleteDialogOpen(false);
      await loadTasks();
    } catch (error) {
      console.error("Error eliminando las tareas", error);
      toast.add({
        type: "error",
        title: "Error al eliminar",
        description:
          error instanceof Error
            ? error.message
            : "No pudimos eliminar las tareas seleccionadas.",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  const startIndex = (currentPage - 1) * itemsPerPage;

  return (
    <div className="flex flex-col space-y-6 w-full mx-auto px-10 py-5">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <nav className="flex w-100 border-b border-gray-200">
          <Link
            to="/tasks"
            aria-current="page"
            className="flex items-center gap-2 border-b-2 border-blue-600 px-3 pb-2.5 text-base font-medium text-blue-600"
          >
            <LayoutList className="w-5 h-5" />
            Lista
          </Link>
          <Link
            to="/calendar"
            className="flex items-center gap-2 border-b-2 border-transparent px-3 pb-2.5 text-base font-medium text-gray-500 transition hover:text-gray-700"
          >
            <Calendar className="w-5 h-5" />
            Calendario
          </Link>
        </nav>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <TaskFilterPopover filters={filters} onApply={handleApplyFilters} />
        </div>
      </div>

      {selectedTasks.length > 0 && (
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 rounded-xl border border-blue-200 bg-blue-50 px-6 py-3">
          <div className="flex items-center gap-2">
            <Checkbox
              checked={
                selectedTasks.length === tasks.length && tasks.length > 0
              }
              onCheckedChange={toggleSelectAll}
              className="border-gray-300 rounded-lg"
            />
            <p className="text-sm text-blue-800 font-medium">
              {selectedTasks.length}{" "}
              {selectedTasks.length === 1
                ? "tarea seleccionada"
                : "tareas seleccionadas"}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              onClick={() => setSelectedTasks([])}
              className="text-gray-700"
            >
              Cancelar
            </Button>
            <Button
              variant="destructive"
              onClick={() => setIsBulkDeleteDialogOpen(true)}
              className="bg-red-600 hover:bg-red-700 text-white"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Eliminar seleccionadas
            </Button>
          </div>
        </div>
      )}

      <div className="rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader className="bg-gray-50/50">
            <TableRow className="hover:bg-transparent border-b-gray-200">
              <TableHead className="w-12.5 pl-6">
                <Checkbox
                  checked={
                    selectedTasks.length === tasks.length && tasks.length > 0
                  }
                  onCheckedChange={toggleSelectAll}
                  className="border-gray-300 rounded-lg"
                />
              </TableHead>
              <TableHead className="font-semibold text-gray-500">
                Tarea
              </TableHead>
              <TableHead className="font-semibold text-gray-500">
                Proyecto
              </TableHead>
              <TableHead className="font-semibold text-gray-500">
                Fecha de Vencimiento
              </TableHead>
              <TableHead className="font-semibold text-gray-500">
                Prioridad
              </TableHead>
              <TableHead className="font-semibold text-gray-500">
                Estado
              </TableHead>
              <TableHead className="w-12.5"></TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {tasks.map((task) => (
              <TableRow
                key={task.id}
                onClick={() => openTaskSheet(task.id)}
                className="hover:bg-gray-50/50 border-b-gray-100 last:border-0 group cursor-pointer"
              >
                <TableCell
                  className="pl-6"
                  onClick={(event) => event.stopPropagation()}
                >
                  <Checkbox
                    checked={selectedTasks.includes(task.id)}
                    onCheckedChange={() => toggleSelectTask(task.id)}
                    className="border-gray-300 rounded-lg"
                  />
                </TableCell>

                <TableCell className="font-medium text-gray-900">
                  {task.title}
                </TableCell>

                <TableCell>
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-6 h-6 rounded bg-blue-500 flex items-center justify-center text-white text-[10px] font-bold`}
                    >
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
                      PRIORITY_CONFIG[task.priority as TaskPriorityEnum]
                        .colorClass
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
                    {
                      COLUMN_STATE_CONFIG[task.columnTitle as ColumnDefaultEnum]
                        .label
                    }
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <div className="border-t border-slate-200 py-4 px-6 bg-slate-50/30 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <p className="text-sm text-slate-500 font-medium">Mostrar</p>
            <Select
              value={itemsPerPage.toString()}
              onValueChange={handleItemsPerPageChange}
            >
              <SelectTrigger className="h-8 w-17.5 bg-white">
                <SelectValue placeholder={itemsPerPage} />
              </SelectTrigger>
              <SelectContent side="top">
                {[5, 10, 20, 50].map((pageSize) => (
                  <SelectItem key={pageSize} value={`${pageSize}`}>
                    {pageSize}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-sm text-slate-500 font-medium">
              registros por página
            </p>
          </div>

          <div className="flex items-center gap-6">
            <p className="text-sm text-slate-500 font-medium hidden md:block">
              {startIndex + 1} -{" "}
              {Math.min(startIndex + itemsPerPage, totalCount)} de {totalCount}
            </p>

            <Pagination className="justify-end w-auto mx-0">
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious
                    href="#"
                    onClick={(e) => handlePageChange(currentPage - 1, e)}
                    className={
                      currentPage === 1
                        ? "pointer-events-none opacity-50"
                        : "cursor-pointer"
                    }
                  />
                </PaginationItem>

                {Array.from({ length: totalPages }).map((_, i) => (
                  <PaginationItem key={i} className="hidden sm:inline-block">
                    <PaginationLink
                      href="#"
                      isActive={currentPage === i + 1}
                      onClick={(e) => handlePageChange(i + 1, e)}
                    >
                      {i + 1}
                    </PaginationLink>
                  </PaginationItem>
                ))}

                <PaginationItem>
                  <PaginationNext
                    href="#"
                    onClick={(e) => handlePageChange(currentPage + 1, e)}
                    className={
                      currentPage === totalPages || totalPages === 0
                        ? "pointer-events-none opacity-50"
                        : "cursor-pointer"
                    }
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </div>
        </div>
      </div>

      <AlertDialog
        open={isBulkDeleteDialogOpen}
        onOpenChange={setIsBulkDeleteDialogOpen}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              {selectedTasks.length}{" "}
              {selectedTasks.length === 1
                ? "tarea seleccionada"
                : "tareas seleccionadas"}
            </AlertDialogTitle>
            <AlertDialogDescription>
              Esta accion eliminara permanentemente {selectedTasks.length}{" "}
              {selectedTasks.length === 1
                ? "la tarea seleccionada"
                : "las tareas seleccionadas"}
              . Esta accion no se puede deshacer.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isDeleting}>
              Cancelar
            </AlertDialogCancel>
            <AlertDialogAction
              onClick={(event) => {
                event.preventDefault();
                handleBulkDelete();
              }}
              disabled={isDeleting}
              className="bg-red-600 hover:bg-red-700"
            >
              {isDeleting ? "Eliminando..." : "Eliminar"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <TaskDetailSheet
        taskId={selectedTaskId}
        open={isTaskSheetOpen}
        onOpenChange={setIsTaskSheetOpen}
        onTaskUpdated={loadTasks}
        onTaskDeleted={loadTasks}
      />
    </div>
  );
};

export default MyTasks;
