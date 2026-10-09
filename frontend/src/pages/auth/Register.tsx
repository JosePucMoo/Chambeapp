import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { authService } from "../../services/auth";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/toast";
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { RegisterRequest } from "@/interfaces/Auth";

const Register = () => {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  const password = watch("password");

  const onSubmit = async (data: RegisterRequest) => {
    try {
      const response = await authService.register(data);

      toast.add({
        type: "success",
        title: "¡Registro exitoso!",
        description: response.message,
      });

      navigate("/auth/login");
    } catch (err) {
      toast.add({
        type: "error",
        title: "Error al registrarse",
        description: err instanceof Error ? err.message : "Error inesperado",
      });
    }
  };

  return (
    <Card className="w-full max-w-md sm:shadow-2xl ring-0 rounded-none px-6">
      <CardHeader className="pb-4 pt-6">
        <CardTitle className="text-center text-4xl font-semibold text-gray-700">
          Crea tu <span className="text-blue-500">cuenta</span>
        </CardTitle>
      </CardHeader>

      <CardContent>
        <form className="mt-0 space-y-4" onSubmit={handleSubmit(onSubmit)}>
          <Field data-invalid={!!errors.name}>
            <FieldLabel
              htmlFor="name"
              className={`text-md font-medium"  ${errors.name ? "" : "text-gray-700"}`}
            >
              Nombre
            </FieldLabel>
            <Input
              id="name"
              type="text"
              placeholder="Tu nombre"
              aria-invalid={!!errors.name}
              className="py-4"
              {...register("name", {
                required: "El nombre es obligatorio",
                minLength: {
                  value: 2,
                  message: "El nombre debe tener al menos 2 caracteres",
                },
              })}
            />
            {errors.name && (
              <FieldDescription>{errors.name?.message}</FieldDescription>
            )}
          </Field>

          <Field data-invalid={!!errors.email}>
            <FieldLabel
              htmlFor="email"
              className={`text-md font-medium"  ${errors.email ? "" : "text-gray-700"}`}
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

          <Field data-invalid={!!errors.password}>
            <FieldLabel
              htmlFor="password"
              className={`text-md font-medium"  ${errors ? "" : "text-gray-700"}`}
            >
              Contraseña
            </FieldLabel>
            <Input
              id="password"
              type="password"
              placeholder="••••••••••••••••"
              aria-invalid={!!errors.password}
              className="py-4"
              {...register("password", {
                required: "La contraseña es obligatoria",
                minLength: {
                  value: 8,
                  message: "La contraseña debe tener al menos 8 caracteres",
                },
              })}
            />
            {errors.password && (
              <FieldDescription>{errors.password?.message}</FieldDescription>
            )}
          </Field>

          <Field data-invalid={!!errors.confirmPassword}>
            <FieldLabel
              htmlFor="confirmPassword"
              className={`text-md font-medium"  ${errors.confirmPassword ? "" : "text-gray-700"}`}
            >
              Repetir contraseña
            </FieldLabel>
            <Input
              id="confirmPassword"
              type="password"
              placeholder="••••••••••••••••"
              aria-invalid={!!errors.confirmPassword}
              className="py-4"
              {...register("confirmPassword", {
                required: "Debes confirmar tu contraseña",
                validate: (value) => {
                  return value === password || "Las contraseñas no coinciden";
                },
              })}
            />
            {errors.confirmPassword && (
              <FieldDescription>
                {errors.confirmPassword?.message}
              </FieldDescription>
            )}
          </Field>

          <nav className="w-full flex flex-col gap-2 2xl:flex-row 2xl:justify-between pt-2">
            <Link
              className="text-gray-500 hover:text-gray-800 transition-colors block text-start text-sm"
              to={"/auth/login"}
            >
              ¿Ya tienes una cuenta?
            </Link>
            <Link
              className="text-gray-500 hover:text-gray-800 transition-colors block text-start text-sm"
              to={"/auth/forgot-password"}
            >
              ¿Olvidaste tu contraseña?
            </Link>
          </nav>

          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-4 mb-2 uppercase bg-blue-500 hover:bg-blue-700 text-white rounded-xs text-base font-bold h-12"
          >
            {isSubmitting ? "Registrando..." : "Crear Cuenta"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default Register;
