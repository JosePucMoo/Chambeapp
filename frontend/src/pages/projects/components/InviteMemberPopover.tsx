import { useState } from "react";
import { useForm } from "react-hook-form";
import { UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Separator } from "@/components/ui/separator";
import {
  Popover,
  PopoverContent,
  PopoverHeader,
  PopoverTitle,
  PopoverTrigger,
} from "@/components/ui/popover";
import { toast } from "@/components/ui/toast";
import { projectService } from "@/services/project";
import type { InviteMemberDTO } from "@/interfaces/Invitation";

interface InviteMemberPopoverProps {
  projectId: string;
}

export const InviteMemberPopover = ({
  projectId,
}: InviteMemberPopoverProps) => {
  const [open, setOpen] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<InviteMemberDTO>({
    defaultValues: { email: "" },
  });

  const handleOpenChange = (nextOpen: boolean) => {
    if (nextOpen) reset();
    setOpen(nextOpen);
  };

  const onSubmit = async (data: InviteMemberDTO) => {
    try {
      await projectService.sendInvitation(projectId, { email: data.email });

      toast.add({
        type: "success",
        title: "Invitación enviada",
        description: `Se envió una invitación a ${data.email}.`,
      });

      reset();
      setOpen(false);
    } catch (error) {
      toast.add({
        type: "error",
        title: "Error al invitar",
        description:
          error instanceof Error
            ? error.message
            : "No pudimos enviar la invitación.",
      });
    }
  };

  return (
    <Popover open={open} onOpenChange={handleOpenChange}>
      <PopoverTrigger
        render={
          <Button
            variant="outline"
            className="hover:cursor-pointer text-slate-700 font-medium h-10 border-slate-300"
          />
        }
      >
        <UserPlus className="w-4 h-4 text-slate-500" />
        Invitar
      </PopoverTrigger>

      <PopoverContent align="end" className="w-80 p-0">
        <PopoverHeader className="gap-0.5 px-4 pt-3.5">
          <PopoverTitle className="text-base text-slate-700">
            Invitar colaborador
          </PopoverTitle>
        </PopoverHeader>

        <Separator />

        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4 p-4">
            <Field data-invalid={!!errors.email}>
              <FieldLabel className="text-sm text-slate-600">
                Correo electrónico
              </FieldLabel>
              <Input
                type="email"
                placeholder="correo@correo.com"
                {...register("email", {
                  required: "El correo es obligatorio",
                  pattern: {
                    value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                    message: "Ingresa un correo electrónico válido",
                  },
                })}
                aria-invalid={!!errors.email}
              />
              {errors.email && <FieldError>{errors.email.message}</FieldError>}
            </Field>

            <p className="text-xs text-slate-400">
              El colaborador debe tener una cuenta en Chambeapp. La invitación
              vence a los 7 días.
            </p>
          </div>

          <Separator />

          <div className="flex items-center justify-between gap-2 p-4">
            <Button
              type="button"
              variant="ghost"
              onClick={() => setOpen(false)}
              className="text-slate-500 hover:cursor-pointer"
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
              className="hover:cursor-pointer bg-blue-500 hover:bg-blue-700"
            >
              {isSubmitting ? "Enviando..." : "Enviar invitación"}
            </Button>
          </div>
        </form>
      </PopoverContent>
    </Popover>
  );
};
