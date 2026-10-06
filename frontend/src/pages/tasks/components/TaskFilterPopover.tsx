import { useState } from "react";
import { Filter, X } from "lucide-react";
import {
  Popover,
  PopoverContent,
  PopoverHeader,
  PopoverTitle,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Field, FieldLabel } from "@/components/ui/field";
import { Separator } from "@/components/ui/separator";
import { ColumnDefaultEnum, TaskPriorityEnum } from "@/interfaces/constants/enums";
import { PRIORITY_CONFIG } from "@/interfaces/constants/taskMappings";
import type { TaskFilters } from "@/interfaces/Task";
import { useProjects } from "@/hooks/useProjects";

const ALL_OPTION = "all";

const EMPTY_FILTERS: TaskFilters = {
  priority: undefined,
  columnTitle: undefined,
  projectId: undefined,
  search: "",
};

interface TaskFilterPopoverProps {
  filters: TaskFilters;
  onApply: (filters: TaskFilters) => void;
}

export function TaskFilterPopover({ filters, onApply }: TaskFilterPopoverProps) {
  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState<TaskFilters>(EMPTY_FILTERS);
  const { projects } = useProjects(1, 50);

  const handleOpenChange = (nextOpen: boolean) => {
    if (nextOpen) setDraft(filters);
    setOpen(nextOpen);
  };

  const activeCount = [
    filters.priority,
    filters.columnTitle,
    filters.projectId,
    filters.search,
  ].filter(Boolean).length;

  const handleApply = () => {
    onApply({ ...draft, search: draft.search?.trim() || undefined });
    setOpen(false);
  };

  const handleClear = () => {
    setDraft(EMPTY_FILTERS);
    onApply(EMPTY_FILTERS);
  };

  return (
    <Popover open={open} onOpenChange={handleOpenChange}>
      <PopoverTrigger
        render={
          <Button
            variant="outline"
            className={`text-gray-700 font-medium h-10 ${
              activeCount > 0 ? "border-blue-300 bg-blue-50" : ""
            }`}
          />
        }
      >
        <Filter className="w-4 h-4 mr-2 text-gray-500" />
        Filtro
        {activeCount > 0 && (
          <span className="ml-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-blue-500 px-1.5 text-xs font-semibold text-white">
            {activeCount}
          </span>
        )}
      </PopoverTrigger>

      <PopoverContent align="end" className="w-80 p-0">
        <PopoverHeader className="gap-0.5 px-4 pt-3.5">
          <PopoverTitle className="text-base text-slate-700">
            Filtrar tareas
          </PopoverTitle>
        </PopoverHeader>

        <Separator />

        <div className="space-y-4 p-4">
          <div className="space-y-2">
            <Field>
              <FieldLabel className="text-sm text-slate-600">
                Buscar por titulo
              </FieldLabel>
              <Input
                placeholder="Ej. diseñar"
                value={draft.search ?? ""}
                onChange={(event) =>
                  setDraft((prev) => ({ ...prev, search: event.target.value }))
                }
              />
            </Field>
          </div>

          <div className="space-y-2">
            <Field>
              <FieldLabel className="text-sm text-slate-600">
                Prioridad
              </FieldLabel>
              <Select
                value={draft.priority ?? ALL_OPTION}
                onValueChange={(value) =>
                  setDraft((prev) => ({
                    ...prev,
                    priority:
                      value === ALL_OPTION
                        ? undefined
                        : (value as TaskPriorityEnum),
                  }))
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Todas las prioridades" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ALL_OPTION}>Todas</SelectItem>
                  {Object.values(TaskPriorityEnum).map((priority) => (
                    <SelectItem key={priority} value={priority}>
                      {PRIORITY_CONFIG[priority].label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>
          </div>

          <div className="space-y-2">
            <Field>
              <FieldLabel className="text-sm text-slate-600">Estado</FieldLabel>
              <Select
                value={draft.columnTitle ?? ALL_OPTION}
                onValueChange={(value) =>
                  setDraft((prev) => ({
                    ...prev,
                    columnTitle: value === ALL_OPTION || !value ? undefined : value,
                  }))
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Todos los estados" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ALL_OPTION}>Todos</SelectItem>
                  {Object.values(ColumnDefaultEnum).map((status) => (
                    <SelectItem key={status} value={status}>
                      {status}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>
          </div>

          <div className="space-y-2">
            <Field>
              <FieldLabel className="text-sm text-slate-600">Proyecto</FieldLabel>
              <Select
                value={draft.projectId ?? ALL_OPTION}
                onValueChange={(value) =>
                  setDraft((prev) => ({
                    ...prev,
                    projectId: value === ALL_OPTION || !value ? undefined : value,
                  }))
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Todos los proyectos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ALL_OPTION}>Todos</SelectItem>
                  {projects.map((project) => (
                    <SelectItem key={project.id} value={project.id}>
                      {project.title}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>
          </div>
        </div>

        <Separator />

        <div className="flex items-center justify-between gap-2 p-4">
          <Button
            variant="ghost"
            onClick={handleClear}
            disabled={activeCount === 0}
            className="text-slate-500"
          >
            <X className="w-4 h-4 mr-1" />
            Limpiar
          </Button>
          <div className="flex items-center gap-2">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancelar
            </Button>
            <Button
              onClick={handleApply}
              className="bg-blue-500 hover:bg-blue-700"
            >
              Aplicar
            </Button>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}