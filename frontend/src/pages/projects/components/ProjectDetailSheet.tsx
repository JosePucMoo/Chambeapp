import { useEffect, useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { AlertCircle } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { DatePickerSimple } from "@/components/ui/datepicker";
import { toast } from "@/components/ui/toast";
import type { Project, UpdateProject } from "@/interfaces/Project";
import { projectService } from "@/services/project";
import { parseDateOnly } from "@/utils/date";

interface ProjectDetailSheetProps {
  projectId: string | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onProjectUpdated?: () => void;
}

export function ProjectDetailSheet({
  projectId,
  open,
  onOpenChange,
  onProjectUpdated,
}: ProjectDetailSheetProps) {
  const [project, setProject] = useState<Project | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isSubmitting },
  } = useForm<UpdateProject>({
    defaultValues: {
      title: "",
      description: "",
      client: "",
      deliveryDate: undefined,
    },
  });

  useEffect(() => {
    if (!open || !projectId) return;

    let active = true;

    const loadProject = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await projectService.get_project_by_id(projectId);

        if (!active) return;

        setProject(response.data);
        reset({
          title: response.data.title,
          description: response.data.description,
          client: response.data.client,
          deliveryDate: parseDateOnly(response.data.deliveryDate),
        });
      } catch (loadError) {
        if (!active) return;

        setProject(null);
        setError(
          loadError instanceof Error
            ? loadError.message
            : "No pudimos cargar el proyecto.",
        );
      } finally {
        if (active) setIsLoading(false);
      }
    };

    loadProject();

    return () => {
      active = false;
    };
  }, [open, projectId, reset]);

  const onSubmit = async (projectData: UpdateProject) => {
    if (!projectId) return;

    try {
      const response = await projectService.update(projectId, projectData);

      toast.add({
        type: "success",
        title: "¡Proyecto actualizado!",
        description: response.message,
      });

      onProjectUpdated?.();
      onOpenChange(false);
    } catch (updateError) {
      toast.add({
        type: "error",
        title: "Error al actualizar",
        description:
          updateError instanceof Error
            ? updateError.message
            : "No pudimos actualizar el proyecto.",
      });
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="w-full sm:max-w-md overflow-y-auto gap-6 p-6 pb-8"
      >
        <SheetHeader className="gap-1.5 p-0">
          <SheetTitle className="text-slate-700 text-xl">
            Editar proyecto
          </SheetTitle>
          <SheetDescription>
            Actualiza la información del proyecto.
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
        ) : !project ? null : (
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-6"
          >
            <div className="space-y-2">
              <Field data-invalid={!!errors.title}>
                <FieldLabel htmlFor="title" className="text-md font-medium">
                  Nombre del Proyecto
                </FieldLabel>
                <Input
                  id="title"
                  placeholder="Ej. Rediseño ChambeApp"
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
                  placeholder="Describe el proyecto de la mejor manera"
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
              <Field data-invalid={!!errors.client}>
                <FieldLabel htmlFor="client" className="text-md font-medium">
                  Cliente / Área
                </FieldLabel>
                <Input
                  id="client"
                  placeholder="Ej. Proyecto interno"
                  {...register("client", {
                    required: "El cliente/area es obligatoria",
                  })}
                  aria-invalid={!!errors.client}
                />
                {errors.client && (
                  <FieldError>{errors.client.message}</FieldError>
                )}
              </Field>
            </div>

            <div className="space-y-2 w-fit">
              <Field data-invalid={!!errors.deliveryDate}>
                <FieldLabel
                  htmlFor="deliveryDate"
                  className="text-md font-medium"
                >
                  Fecha de entrega
                </FieldLabel>
                <Controller
                  name="deliveryDate"
                  control={control}
                  rules={{ required: "La fecha de entrega es obligatoria" }}
                  render={({ field }) => (
                    <DatePickerSimple
                      date={field.value}
                      onChange={field.onChange}
                      placeholder="Selecciona la fecha límite"
                    />
                  )}
                />
                {errors.deliveryDate && (
                  <FieldError>{errors.deliveryDate.message}</FieldError>
                )}
              </Field>
            </div>

            <SheetFooter className="mt-1 gap-2 border-t-0 bg-transparent p-0 sm:justify-end">
              <div className="flex flex-col-reverse gap-2 sm:flex-row">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => onOpenChange(false)}
                  className="hover:cursor-pointer"
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="bg-blue-500 hover:bg-blue-700 hover:cursor-pointer"
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
