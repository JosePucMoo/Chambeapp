import { useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { toast } from "@/components/ui/toast";
import { FieldLabel, Field, FieldError } from "@/components/ui/field";
import { Textarea } from "@/components/ui/textarea";
import { DatePickerSimple } from "@/components/ui/datepicker";
import type { CreateTask } from "@/interfaces/Task";
import { useProjectMembers } from "@/hooks/useProjectMembers";
import { AssigneeSelect } from "./AssigneSelect";
import { taskService } from "@/services/task";
import { PrioritySelect } from "./PrioritySelect";

interface CreateTaskDialogProps {
  projectId: string;
  loadTasks: () => void;
}

export function CreateTaskDialog({ projectId }: CreateTaskDialogProps) {
  const [open, setOpen] = useState(false);
  const { members } = useProjectMembers(projectId);

  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isSubmitting },
  } = useForm<CreateTask>({
    defaultValues: {
      title: "",
      description: "",
      priority: undefined,
      dueDate: undefined,
      assigneeId: "",
    },
  });

  const onSubmit = async (task: CreateTask) => {
    try {
      const response = await taskService.create(task, projectId);

      toast.add({
        type: "success",
        title: "¡Registro exitoso!",
        description: response.message,
      });

      reset();
      setOpen(false);
    } catch (error: any) {
      toast.add({
        type: "error",
        title: "Error al crear",
        description: error.message,
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger
        render={
          <Button className="bg-blue-500 hover:bg-blue-700 text-white font-medium h-10">
            <Plus className="w-4 h-4" />
            Nueva tarea
          </Button>
        }
      />

      <DialogContent className="sm:max-w-md">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle className="text-slate-700 text-xl">
              Crear Nueva Tarea
            </DialogTitle>
            <DialogDescription>
              Define bien tu tarea y comienza a chambear
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-6">
            <div className="space-y-2">
              <Field data-invalid={!!errors.title}>
                <FieldLabel
                  htmlFor="title"
                  className={`text-md font-medium" ${!!errors.title ? "" : "text-slate-700"}`}
                >
                  Titulo de la tarea
                </FieldLabel>
                <Input
                  id="title"
                  placeholder="Ej. Diseñar arquitectura"
                  {...register("title", {
                    required: "El titulo es obligatorio",
                    minLength: {
                      value: 3,
                      message: "El titulo debe tener al menos 3 caracteres",
                    },
                    maxLength: {
                      value: 50,
                      message: "El titulo no puede exceder los 50 caracteres",
                    },
                  })}
                  aria-invalid={!!errors.title}
                />
                {errors.title && (
                  <FieldError>{errors.title.message}</FieldError>
                )}
              </Field>
            </div>

            <div className="space-y-2">
              <Field data-invalid={!!errors.description}>
                <FieldLabel
                  htmlFor="description"
                  className={`text-md font-medium" ${!!errors.description ? "" : "text-slate-700"}`}
                >
                  Descripción
                </FieldLabel>
                <Textarea
                  id="description"
                  placeholder="Describe tu tarea de la mejor manera"
                  {...register("description", {
                    required: "La descripción es obligatoria",
                  })}
                  aria-invalid={!!errors.description}
                />
                {errors.description && (
                  <FieldError>{errors.description.message}</FieldError>
                )}
              </Field>
            </div>

            <div className="space-y-2">
              <PrioritySelect control={control} />
            </div>

            <div className="space-y-2">
              <AssigneeSelect control={control} members={members} />
            </div>

            <div className="space-y-2 w-fit">
              <Field data-invalid={!!errors.dueDate}>
                <FieldLabel
                  htmlFor="dueDate"
                  className={`text-md font-medium" ${!!errors.dueDate ? "" : "text-slate-700"}`}
                >
                  Fecha de vencimiento
                </FieldLabel>

                <Controller
                  name="dueDate"
                  control={control}
                  rules={{ required: "La fecha de vencimiento es obligatoria" }}
                  render={({ field }) => (
                    <DatePickerSimple
                      date={field.value}
                      onChange={field.onChange}
                      placeholder="Selecciona la fecha límite"
                    />
                  )}
                />

                {errors.dueDate && (
                  <FieldError>{errors.dueDate.message}</FieldError>
                )}
              </Field>
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
              className="bg-blue-500 hover:bg-blue-700"
            >
              {isSubmitting ? "Guardando..." : "Crear Tarea"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
