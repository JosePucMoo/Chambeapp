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
import {
  Calendar,
  CalendarDays,
  Filter,
  LayoutList,
  MoreHorizontal,
  Plus,
} from "lucide-react";
import { useOutletContext } from "react-router-dom";
import type { LayoutContextType } from "@/interfaces/Context";

const tasks = [
  {
    id: "1",
    name: "Project Kick Off",
    project: "InterActive",
    projectColor: "bg-red-600",
    date: "06 September 2024",
    status: "Backlog",
    progress: 70,
  },
  {
    id: "2",
    name: "Whiteboarding",
    project: "InterActive",
    projectColor: "bg-red-500",
    date: "06 September 2024",
    status: "Backlog",
    progress: 70,
  },
  {
    id: "3",
    name: "Brainstorming",
    project: "MyHotel",
    projectColor: "bg-red-600",
    date: "06 September 2024",
    status: "To-Do",
    progress: 70,
  },
  {
    id: "4",
    name: "Wireframe",
    project: "MyHotel",
    projectColor: "bg-red-500",
    date: "06 September 2024",
    status: "To-Do",
    progress: 70,
  },
  {
    id: "5",
    name: "Prototyping",
    project: "InterActive",
    projectColor: "bg-red-700",
    date: "06 September 2024",
    status: "In Progress",
    progress: 70,
  },
  {
    id: "6",
    name: "Landing Page",
    project: "InterActive",
    projectColor: "bg-red-600",
    date: "06 September 2024",
    status: "In Progress",
    progress: 70,
  },
  {
    id: "7",
    name: "Product Page",
    project: "InAct",
    projectColor: "bg-black",
    date: "06 September 2024",
    status: "Backlog",
    progress: 70,
  },
  {
    id: "8",
    name: "Contact Page",
    project: "MyAccounting",
    projectColor: "bg-red-600",
    date: "06 September 2024",
    status: "To-Do",
    progress: 70,
  },
  {
    id: "9",
    name: "API Test",
    project: "MyAccounting",
    projectColor: "bg-red-600",
    date: "06 September 2024",
    status: "Done",
    progress: 70,
  },
  {
    id: "10",
    name: "Automation",
    project: "InAct",
    projectColor: "bg-red-600",
    date: "06 September 2024",
    status: "Done",
    progress: 70,
  },
];

const getStatusBadge = (status: string) => {
  switch (status) {
    case "Backlog":
      return (
        <Badge className="bg-gray-800 hover:bg-gray-700 text-white font-normal rounded-full px-3">
          {status}
        </Badge>
      );
    case "To-Do":
      return (
        <Badge className="bg-blue-400 hover:bg-blue-500 text-white font-normal rounded-full px-3">
          {status}
        </Badge>
      );
    case "In Progress":
      return (
        <Badge className="bg-orange-400 hover:bg-orange-500 text-white font-normal rounded-full px-3">
          {status}
        </Badge>
      );
    case "Done":
      return (
        <Badge className="bg-emerald-500 hover:bg-emerald-600 text-white font-normal rounded-full px-3">
          {status}
        </Badge>
      );
    default:
      return <Badge>{status}</Badge>;
  }
};

function MyTasks() {
  const [selectedTasks, setSelectedTasks] = useState<string[]>([]);
  const { setPageTitle } = useOutletContext<LayoutContextType>();

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

  return (
    <div className="flex flex-col space-y-6 w-full mx-auto">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-gray-200 pb-4">
        <Tabs defaultValue="list" className="w-100">
          <TabsList className="bg-transparent h-12 p-0">
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
          <Button className="bg-blue-600 hover:bg-blue-700 text-white font-medium h-10">
            <Plus className="w-4 h-4 mr-2" />
            Agregar nuevo
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
                Estado
              </TableHead>
              <TableHead className="w-12.5"></TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {tasks.map((task) => (
              <TableRow
                key={task.id}
                className="hover:bg-gray-50/50 border-b-gray-100 last:border-0 group"
              >
                <TableCell className="pl-6">
                  <Checkbox
                    checked={selectedTasks.includes(task.id)}
                    onCheckedChange={() => toggleSelectTask(task.id)}
                    className="border-gray-300 rounded-lg"
                  />
                </TableCell>

                <TableCell className="font-medium text-gray-900">
                  {task.name}
                </TableCell>

                <TableCell>
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-6 h-6 rounded ${task.projectColor} flex items-center justify-center text-white text-[10px] font-bold`}
                    >
                      {task.project.charAt(0)}
                    </div>
                    <span className="text-gray-600">{task.project}</span>
                  </div>
                </TableCell>

                <TableCell>
                  <div className="flex items-center text-gray-600 font-medium gap-2 text-sm">
                    <CalendarDays className="w-4 h-4 text-gray-400" />
                    {task.date}
                  </div>
                </TableCell>

                <TableCell>{getStatusBadge(task.status)}</TableCell>

                <TableCell className="pr-6">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-gray-400 group-hover:opacity-100 transition-opacity"
                  >
                    <MoreHorizontal className="h-5 w-5" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

export default MyTasks;
