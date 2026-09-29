import { useState } from "react";
import { useForm } from "react-hook-form";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
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

interface CreateProjectForm {
  name: string;
  client: string;
}

export function CreateProjectDialog() {
  const [open, setOpen] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateProjectForm>();

  const onSubmit = async (data: CreateProjectForm) => {
    try {
      console.log("Datos a enviar:", data);

      toast.add({
        type: "success",
        title: "Proyecto creado",
        description: `El proyecto ${data.name} ha sido creado exitosamente.`,
      });

      reset();
      setOpen(false);
    } catch (error) {
      toast.add({
        type: "error",
        title: "Error al crear",
        description: "Hubo un problema al crear el proyecto.",
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white font-medium h-10">
          <Plus className="w-4 h-4 mr-2" />
          Nuevo Proyecto
        </Button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-106">
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
              <Label
                htmlFor="name"
                className={errors.name ? "text-red-500" : ""}
              >
                Nombre del Proyecto
              </Label>
              <Input
                id="name"
                placeholder="Ej. Rediseño ChambeApp"
                {...register("name", { required: "El nombre es obligatorio" })}
                aria-invalid={!!errors.name}
              />
              {errors.name && (
                <span className="text-xs text-red-500">
                  {errors.name.message}
                </span>
              )}
            </div>

            <div className="space-y-2">
              <Label
                htmlFor="client"
                className={errors.client ? "text-red-500" : ""}
              >
                Cliente o Área
              </Label>
              <Input
                id="client"
                placeholder="Ej. Producto Interno"
                {...register("client", {
                  required: "El cliente es obligatorio",
                })}
              />
              {errors.client && (
                <span className="text-xs text-red-500">
                  {errors.client.message}
                </span>
              )}
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
