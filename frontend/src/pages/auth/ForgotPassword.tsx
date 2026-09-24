import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/toast";
import type { ForgotPasswordRequest } from "@/interfaces/AuthResponse";
import { authService } from "@/services/auth";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

const ForgotPassword = () => {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = async (data: ForgotPasswordRequest) => {
    try {
      const response = await authService.forgotPassword(data);
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
          Recupera tu <span className="text-blue-500 font-bold">acceso</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form className="mt-5 space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <Field data-invalid={!!errors.email}>
            <FieldLabel
              htmlFor="email"
              className={`text-md font-medium"  ${!!errors.email ? "" : "text-gray-700"}`}
            >
              Correo Electrónico
            </FieldLabel>

            <Input
              id="email"
              type="email"
              placeholder="correo@correo.com"
              aria-invalid={!!errors.email}
              className="py-4"
              {...register("email", {
                required: "El correo es obligatorio",
                pattern: {
                  value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                  message: "Ingresa un correo electrónico válido",
                },
              })}
            />
            {errors.email && (
              <FieldDescription>{errors.email?.message}</FieldDescription>
            )}
          </Field>
          <nav className="w-full flex flex-col gap-1 2xl:flex-row 2xl:justify-between">
            <Link className="text-gray-500 block text-start text-sm" to={"/"}>
              ¿Ya tienes una cuenta?
            </Link>
            <Link
              className="text-gray-500 block text-start text-sm"
              to={"/forgot-password"}
            >
              ¿No tienes una cuenta?
            </Link>
          </nav>

          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-4 mb-2 uppercase bg-blue-500 hover:bg-blue-700 text-white rounded-xs text-base font-bold h-12"
          >
            {isSubmitting ? "Enviando..." : "Enviar Instrucciones"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default ForgotPassword;
