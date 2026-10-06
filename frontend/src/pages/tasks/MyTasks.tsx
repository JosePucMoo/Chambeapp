import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Calendar, CalendarDays, Filter, LayoutList } from "lucide-react";
import { useOutletContext } from "react-router-dom";
import type { LayoutContextType } from "@/interfaces/Context";
import {
  COLUMN_STATE_CONFIG,
  PRIORITY_CONFIG,
} from "@/interfaces/constants/taskMappings";
import {
  ColumnDefaultEnum,
  TaskPriorityEnum,
} from "@/interfaces/constants/enums";
import { useTasks } from "@/hooks/useTasks";
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

function MyTasks() {
  const [selectedTasks, setSelectedTasks] = useState<string[]>([]);
  const { setPageTitle } = useOutletContext<LayoutContextType>();
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  const { tasks, totalCount, totalPages, loadTasks } = useTasks(
    currentPage,
    itemsPerPage,
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

  const handlePageChange = (page: number, e: React.MouseEvent) => {
    e.preventDefault();
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const handleItemsPerPageChange = (value: string | null) => {
    if (!value) return;
    setItemsPerPage(Number(value));
    setCurrentPage(1);
  };

  const startIndex = (currentPage - 1) * itemsPerPage;

  return (
    <div className="flex flex-col space-y-6 w-full mx-auto px-10 py-5">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <Tabs defaultValue="list" className="w-100 ">
          <TabsList className="bg-transparent p-0 border-b border-gray-200 rounded-none">
            <TabsTrigger
              value="list"
              className="data-active:text-blue-600 data-active:border-b-blue-600 text-gray-500 rounded-none font-medium text-base gap-2 px-3"
            >
              <LayoutList className="w-5 h-5" />
              Lista
            </TabsTrigger>
            <TabsTrigger
              value="calendary"
              className="data-active:text-blue-600 data-active:border-b-blue-600 text-gray-500 rounded-none font-medium text-base gap-2 px-3"
            >
              <Calendar className="w-5 h-5" />
              Calendario
            </TabsTrigger>
          </TabsList>
        </Tabs>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <Button variant="outline" className="text-gray-700 font-medium h-10">
            <Filter className="w-4 h-4 mr-2 text-gray-500" />
            Filtro
          </Button>
        </div>
      </div>

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

      <TaskDetailSheet
        taskId={selectedTaskId}
        open={isTaskSheetOpen}
        onOpenChange={setIsTaskSheetOpen}
        onTaskUpdated={loadTasks}
        onTaskDeleted={loadTasks}
      />
    </div>
  );
}

export default MyTasks;
