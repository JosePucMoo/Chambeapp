import { useEffect, useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { AlertCircle, Trash2 } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { DatePickerSimple } from "@/components/ui/datepicker";
import { toast } from "@/components/ui/toast";
import { AssigneeSelect } from "@/pages/projects/components/AssigneSelect";
import { PrioritySelect } from "@/pages/projects/components/PrioritySelect";
import { COLUMN_STATE_CONFIG } from "@/interfaces/constants/taskMappings";
import { ColumnDefaultEnum } from "@/interfaces/constants/enums";
import type { TaskDetail, UpdateTask } from "@/interfaces/Task";
import { useProjectMembers } from "@/hooks/useProjectMembers";
import { taskService } from "@/services/task";

interface TaskDetailSheetProps {
  taskId: string | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onTaskUpdated?: () => void;
  onTaskDeleted?: () => void;
}

export function TaskDetailSheet({
  taskId,
  open,
  onOpenChange,
  onTaskUpdated,
  onTaskDeleted,
}: TaskDetailSheetProps) {
  const [task, setTask] = useState<TaskDetail | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const { members } = useProjectMembers(task?.projectId ?? "");

  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isSubmitting },
  } = useForm<UpdateTask>({
    defaultValues: {
      title: "",
      description: "",
      priority: undefined,
      dueDate: undefined,
      assigneeId: "",
    },
  });

  useEffect(() => {
    if (!open || !taskId) return;

    let active = true;

    const loadTask = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await taskService.get_by_id(taskId);

        if (!active) return;

        const taskDetail = response.data;

        setTask(taskDetail);
        reset({
          title: taskDetail.title,
          description: taskDetail.description,
          priority: taskDetail.priority,
          dueDate: new Date(taskDetail.dueDate),
          assigneeId: taskDetail.assigneeId,
        });
      } catch (loadError) {
        if (!active) return;

        setTask(null);
        setError(
          loadError instanceof Error
            ? loadError.message
            : "No pudimos cargar la tarea.",
        );
      } finally {
        if (active) setIsLoading(false);
      }
    };

    loadTask();

    return () => {
      active = false;
    };
  }, [open, taskId, reset]);

  const onSubmit = async (taskData: UpdateTask) => {
    if (!taskId) return;

    try {
      const response = await taskService.update(taskData, taskId);

      toast.add({
        type: "success",
        title: "¡Tarea actualizada!",
        description: response.message,
      });

      onTaskUpdated?.();
      onOpenChange(false);
    } catch (updateError) {
      toast.add({
        type: "error",
        title: "Error al actualizar",
        description:
          updateError instanceof Error
            ? updateError.message
            : "No pudimos actualizar la tarea.",
      });
    }
  };

  const handleDelete = async () => {
    if (!taskId) return;

    setIsDeleting(true);

    try {
      const response = await taskService.delete(taskId);

      toast.add({
        type: "success",
        title: "¡Tarea eliminada!",
        description: response.message,
      });

      onTaskDeleted?.();
      onOpenChange(false);
    } catch (deleteError) {
      toast.add({
        type: "error",
        title: "Error al eliminar",
        description:
          deleteError instanceof Error
            ? deleteError.message
            : "No pudimos eliminar la tarea.",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  const columnConfig = task
    ? COLUMN_STATE_CONFIG[task.columnTitle as ColumnDefaultEnum]
    : null;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="w-full sm:max-w-md overflow-y-auto gap-6 p-6 pb-8"
      >
        <SheetHeader className="gap-1.5 p-0">
          <SheetTitle className="text-slate-700 text-xl">
            Detalle de la tarea
          </SheetTitle>
          <SheetDescription>
            Actualiza la información de la tarea o elimínala.
          </SheetDescription>
        </SheetHeader>

        {isLoading ? (
          <div className="space-y-4">
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
          </div>
        ) : error ? (
          <div className="flex flex-col items-center gap-3 py-10 text-center">
            <AlertCircle className="text-rose-500 w-6 h-6" />
            <p className="text-sm text-slate-600">{error}</p>
          </div>
        ) : !task ? null : (
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-6"
          >
            {task.projectTitle && (
              <div className="flex items-center gap-2">
                <span className="text-sm text-slate-500">
                  {task.projectTitle}
                </span>
                {columnConfig && (
                  <Badge className={columnConfig.colorClass}>
                    {columnConfig.label}
                  </Badge>
                )}
              </div>
            )}

            <div className="space-y-2">
              <Field data-invalid={!!errors.title}>
                <FieldLabel htmlFor="title" className="text-md font-medium">
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
                  className="text-md font-medium"
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
                <FieldLabel htmlFor="dueDate" className="text-md font-medium">
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

            <SheetFooter className="mt-1 gap-2 border-t-0 bg-transparent p-0 sm:justify-between">
              <AlertDialog>
                <AlertDialogTrigger
                  render={
                    <Button
                      type="button"
                      variant="outline"
                      className="text-rose-600 border-rose-200 hover:bg-rose-50 hover:text-rose-700"
                    />
                  }
                >
                  <Trash2 className="w-4 h-4" />
                  Eliminar
                </AlertDialogTrigger>

                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle className="text-slate-700">
                      ¿Eliminar esta tarea?
                    </AlertDialogTitle>
                    <AlertDialogDescription>
                      La tarea &quot;{task.title}&quot; se eliminará de forma
                      permanente. Esta acción no se puede deshacer.
                    </AlertDialogDescription>
                  </AlertDialogHeader>

                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction
                      onClick={handleDelete}
                      disabled={isDeleting}
                      className="bg-rose-600 hover:bg-rose-700"
                    >
                      {isDeleting ? "Eliminando..." : "Sí, eliminar"}
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>

              <div className="flex flex-col-reverse gap-2 sm:flex-row">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => onOpenChange(false)}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="bg-blue-500 hover:bg-blue-700"
                >
                  {isSubmitting ? "Guardando..." : "Guardar cambios"}
                </Button>
              </div>
            </SheetFooter>
          </form>
        )}
      </SheetContent>
    </Sheet>
  );
}
