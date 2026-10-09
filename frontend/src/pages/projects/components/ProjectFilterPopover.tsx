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
import { ProjectStatusEnum, RoleEnum } from "@/interfaces/constants/enums";
import type { ProjectFilters } from "@/interfaces/Project";

const ALL_OPTION = "all";

const EMPTY_FILTERS: ProjectFilters = {
  search: "",
  status: undefined,
  role: undefined,
};

interface ProjectFilterPopoverProps {
  filters: ProjectFilters;
  onApply: (filters: ProjectFilters) => void;
}

export const ProjectFilterPopover = ({
  filters,
  onApply,
}: ProjectFilterPopoverProps) => {
  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState<ProjectFilters>(EMPTY_FILTERS);

  const handleOpenChange = (nextOpen: boolean) => {
    if (nextOpen) setDraft(filters);
    setOpen(nextOpen);
  };

  const activeCount = [filters.search, filters.status, filters.role].filter(
    Boolean,
  ).length;

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
            className={`hover:cursor-pointer text-slate-700 font-medium h-10 border-slate-300 ${
              activeCount > 0 ? "border-blue-300 bg-blue-50" : ""
            }`}
          />
        }
      >
        <Filter className="w-4 h-4 mr-2 text-slate-500" />
        Filtrar
        {activeCount > 0 && (
          <span className="ml-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-blue-500 px-1.5 text-xs font-semibold text-white">
            {activeCount}
          </span>
        )}
      </PopoverTrigger>

      <PopoverContent align="end" className="w-80 p-0">
        <PopoverHeader className="gap-0.5 px-4 pt-3.5">
          <PopoverTitle className="text-base text-slate-700">
            Filtrar proyectos
          </PopoverTitle>
        </PopoverHeader>

        <Separator />

        <div className="space-y-4 p-4">
          <div className="space-y-2">
            <Field>
              <FieldLabel className="text-sm text-slate-600">
                Buscar por nombre
              </FieldLabel>
              <Input
                placeholder="Ej. Chambeapp"
                value={draft.search ?? ""}
                onChange={(event) =>
                  setDraft((prev) => ({
                    ...prev,
                    search: event.target.value,
                  }))
                }
              />
            </Field>
          </div>

          <div className="space-y-2">
            <Field>
              <FieldLabel className="text-sm text-slate-600">Estado</FieldLabel>
              <Select
                value={draft.status ?? ALL_OPTION}
                onValueChange={(value) =>
                  setDraft((prev) => ({
                    ...prev,
                    status:
                      value === ALL_OPTION
                        ? undefined
                        : (value as ProjectFilters["status"]),
                  }))
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Todos los estados" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ALL_OPTION}>Todos</SelectItem>
                  {Object.values(ProjectStatusEnum).map((status) => (
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
              <FieldLabel className="text-sm text-slate-600">Rol</FieldLabel>
              <Select
                value={draft.role ?? ALL_OPTION}
                onValueChange={(value) =>
                  setDraft((prev) => ({
                    ...prev,
                    role:
                      value === ALL_OPTION
                        ? undefined
                        : (value as ProjectFilters["role"]),
                  }))
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Todos los roles" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ALL_OPTION}>Todos</SelectItem>
                  {Object.values(RoleEnum).map((role) => (
                    <SelectItem key={role} value={role}>
                      {role}
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
            className="text-slate-500 hover:cursor-pointer"
          >
            <X className="w-4 h-4 mr-1" />
            Limpiar
          </Button>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              onClick={() => setOpen(false)}
              className="hover:cursor-pointer"
            >
              Cancelar
            </Button>
            <Button
              onClick={handleApply}
              className="bg-blue-500 hover:bg-blue-700 hover:cursor-pointer"
            >
              Aplicar
            </Button>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
};
