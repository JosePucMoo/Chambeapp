import { useState } from "react";
import { Column } from "./Column";
import type { Task } from "@/interfaces/Task";
import { DragDropProvider } from "@dnd-kit/react";

const TAREAS_INICIALES: Task[] = [
  {
    id: "1",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "2",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "3",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "4",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "5",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "6",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "7",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "8",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "9",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "10",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "11",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "12",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "13",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "14",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
  {
    id: "15",
    title: "Diseñar UI del Dashboard",
    description: "Mi descripcion",
    priority: "High",
    columnId: "1",
    dueDate: new Date(2026, 12, 24),
  },
  {
    id: "16",
    title: "Configurar PostgreSQL",
    priority: "Low",
    description: "Mi descripcion",
    columnId: "2",
    dueDate: new Date(2026, 5, 24),
  },
];

export function Board() {
  const [tasks, setTasks] = useState<Task[]>(TAREAS_INICIALES);

  const handleDragEnd = (event: any) => {
    if (event.canceled || !event.operation.target) return;

    const activeId = event.operation.source.id;
    const overId = event.operation.target.id;

    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === activeId ? { ...task, columnId: overId } : task,
      ),
    );
  };

  return (
    <DragDropProvider onDragEnd={handleDragEnd}>
      <div className="flex gap-6 overflow-x-auto justify-between m-0 flex-1 overflow-y-hidden h-full">
        <Column
          id="1"
          title="Por Hacer"
          tasks={tasks.filter((t) => t.columnId === "1")}
        />
        <Column
          id="2"
          title="En Progreso"
          tasks={tasks.filter((t) => t.columnId === "2")}
        />
        <Column
          id="3"
          title="En revision"
          tasks={tasks.filter((t) => t.columnId === "3")}
        />
        <Column
          id="4"
          title="Ultima reviison xd"
          tasks={tasks.filter((t) => t.columnId === "4")}
        />
        <Column
          id="5"
          title="Completado"
          tasks={tasks.filter((t) => t.columnId === "5")}
        />
      </div>
    </DragDropProvider>
  );
}
