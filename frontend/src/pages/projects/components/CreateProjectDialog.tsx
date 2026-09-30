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
import type { CreateProject } from "@/interfaces/Project";
import { FieldLabel, Field, FieldDescription } from "@/components/ui/field";
import { Textarea } from "@/components/ui/textarea";
import { DatePickerSimple } from "@/components/ui/datepicker";
import { projectService } from "@/services/project";

interface CreateProjectDialogProps {
  loadProyects: () => void;
}

export function CreateProjectDialog({
  loadProyects,
}: CreateProjectDialogProps) {
  const [open, setOpen] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isSubmitting },
  } = useForm<CreateProject>({
    defaultValues: {
      title: "",
      description: "",
      client: "",
      deliveryDate: undefined,
    },
  });

  const onSubmit = async (data: CreateProject) => {
    try {
      const response = await projectService.create(data);

      loadProyects();

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
          <Button className="bg-blue-600 hover:bg-blue-700 text-white font-medium h-10">
            <Plus className="w-4 h-4 mr-2" />
            Nuevo Proyecto
          </Button>
        }
      />

      <DialogContent className="sm:max-w-md">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Crear Nuevo Proyecto</DialogTitle>
            <DialogDescription>
              Configura los detalles iniciales. Podrás invitar a tu equipo más
              adelante.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-6">
            <div className="space-y-2">
              <Field data-invalid={!!errors.title}>
                <FieldLabel
                  htmlFor="title"
                  className={`text-md font-medium" ${!!errors.title ? "" : "text-gray-700"}`}
                >
                  Nombre del Proyecto
                </FieldLabel>
                <Input
                  id="title"
                  placeholder="Ej. Rediseño ChambeApp"
                  {...register("title", {
                    required: "El titulo es obligatorio",
                  })}
                  aria-invalid={!!errors.title}
                />
                {errors.title && (
                  <FieldDescription>{errors.title.message}</FieldDescription>
                )}
              </Field>
            </div>

            <div className="space-y-2">
              <Field data-invalid={!!errors.description}>
                <FieldLabel
                  htmlFor="description"
                  className={`text-md font-medium" ${!!errors.description ? "" : "text-gray-700"}`}
                >
                  Descripción
                </FieldLabel>
                <Textarea
                  id="description"
                  placeholder="Mi primer proyecto personal"
                  {...register("description", {
                    required: "La descripción es obligatoria",
                  })}
                  aria-invalid={!!errors.description}
                />
                {errors.description && (
                  <FieldDescription>
                    {errors.description.message}
                  </FieldDescription>
                )}
              </Field>
            </div>

            <div className="space-y-2">
              <Field data-invalid={!!errors.client}>
                <FieldLabel
                  htmlFor="description"
                  className={`text-md font-medium" ${!!errors.client ? "" : "text-gray-700"}`}
                >
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
                  <FieldDescription>{errors.client.message}</FieldDescription>
                )}
              </Field>
            </div>

            <div className="space-y-2 w-fit">
              <Field data-invalid={!!errors.deliveryDate}>
                <FieldLabel
                  htmlFor="deliveryDate"
                  className={`text-md font-medium" ${!!errors.deliveryDate ? "" : "text-gray-700"}`}
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
                  <FieldDescription>
                    {errors.deliveryDate.message}
                  </FieldDescription>
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
              className="bg-blue-600 hover:bg-blue-700"
            >
              {isSubmitting ? "Guardando..." : "Crear Proyecto"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
