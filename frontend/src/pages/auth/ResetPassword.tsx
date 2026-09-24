import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Field, FieldLabel, FieldDescription } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/toast";
import type { ResetPasswordRequest } from "@/interfaces/Auth";
import { authService } from "@/services/auth";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";

const ResetPassword = () => {
  const params = useParams();
  const token = params.token || "";
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      newPassword: "",
      confirmPassword: "",
    },
  });

  const newPassword = watch("newPassword");

  const onSubmit = async (data: ResetPasswordRequest) => {
    try {
      const response = await authService.resetPassword(token, data);
      toast.add({
        type: "success",
        title: "Cambios guardados",
        description: response.message,
      });
      navigate("/");
    } catch (error: any) {
      toast.add({
        type: "error",
        title: "Cambios no guardados",
        description: error.message,
      });
    }
  };

  return (
    <Card className="w-full max-w-md sm:shadow-2xl ring-0 rounded-none px-6">
      <CardHeader>
        <CardTitle className="block text-center text-gray-700 text-4xl font-semibold mt-5">
          Crea tu nueva <span className="text-blue-500">contraseña</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form className="mt-5 space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <Field data-invalid={!!errors.newPassword}>
            <FieldLabel
              className={`block text-md font-medium ${!!errors.newPassword ? "" : "text-gray-700"}`}
            >
              Nueva contraseña
            </FieldLabel>
            <Input
              type="password"
              placeholder="••••••••••••••••"
              className="border border-gray-300 w-full p-2 mt-2 bg-gray-50 rounded-xl"
              {...register("newPassword", {
                required: "La contraseña es obligatoria",
                minLength: {
                  value: 8,
                  message: "La contraseña debe tener al menos 8 caracteres",
                },
              })}
              aria-invalid={!!errors.newPassword}
            />
            {errors.newPassword && (
              <FieldDescription>{errors.newPassword?.message}</FieldDescription>
            )}
          </Field>
          <Field data-invalid={!!errors.confirmPassword}>
            <FieldLabel
              className={`block text-md font-medium ${!!errors.confirmPassword ? "" : "text-gray-700"}`}
            >
              Confirmar contraseña
            </FieldLabel>
            <Input
              type="password"
              placeholder="••••••••••••••••"
              className="border border-gray-300 w-full p-2 mt-2 bg-gray-50 rounded-xl"
              {...register("confirmPassword", {
                required: "La contraseña es obligatoria",
                minLength: {
                  value: 8,
                  message: "La contraseña debe tener al menos 8 caracteres",
                },
                validate: (value) => {
                  value === newPassword || "Las contraseñas no coinciden";
                },
              })}
              aria-invalid={!!errors.confirmPassword}
            />
            {errors.confirmPassword && (
              <FieldDescription>
                {errors.confirmPassword?.message}
              </FieldDescription>
            )}
          </Field>
          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-4 mb-2 uppercase bg-blue-500 hover:bg-blue-700 text-white rounded-xs text-base font-bold h-12"
          >
            {isSubmitting ? "Guardando..." : "Guardar Contraseña"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default ResetPassword;
