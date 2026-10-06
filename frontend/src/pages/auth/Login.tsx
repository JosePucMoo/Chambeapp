import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import { useForm } from "react-hook-form";
import { authService } from "@/services/auth";
import type { LoginRequest } from "@/interfaces/Auth";
import { toast } from "@/components/ui/toast";
import { useAuth } from "@/hooks/useAuth";

const Login = () => {
  const { login } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const navigate = useNavigate();

  const onSubmit = async (data: LoginRequest) => {
    try {
      const response = await authService.login(data);
      const token = response.data?.token || "";
      const user = response.data?.user;

      login(token, user);
      toast.add({
        type: "success",
        title: "¡Bienvenido a Chambeapp!",
      });
      navigate("/");
    } catch (error) {
      toast.add({
        type: "error",
        title: "Error al iniciar sesión",
        description:
          error instanceof Error ? error.message : "Error inesperado",
      });
    }
  };

  return (
    <Card className="w-full max-w-md border-none rounded-none ring-0 sm:shadow-2xl px-6">
      <CardHeader className="mb-4 mt-6 justify-center">
        <CardTitle className="block text-center text-gray-700 text-4xl font-semibold">
          Inicio de <span className="text-blue-500">sesión</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-0 space-y-4">
          <Field data-invalid={!!errors.email}>
            <FieldLabel
              htmlFor="email"
              className={`text-md font-medium ${errors.email ? "" : "text-gray-800"}`}
            >
              Correo Electrónico
            </FieldLabel>
            <Input
              id="email"
              type="email"
              placeholder="correo@correo.com"
              className="bg-gray-50 rounded-xl h-11"
              {...register("email", {
                required: "El correo es obligatorio",
                pattern: {
                  value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                  message: "Ingresa un correo electrónico válido",
                },
              })}
              aria-invalid={!!errors.email}
            />
            {errors.email && (
              <FieldDescription>{errors.email?.message}</FieldDescription>
            )}
          </Field>

          <Field data-invalid={!!errors.password}>
            <FieldLabel
              htmlFor="password"
              className={`text-md font-medium ${errors.password ? "" : "text-gray-800"}`}
            >
              Contraseña
            </FieldLabel>
            <Input
              id="password"
              type="password"
              placeholder="••••••••••••••••"
              className="bg-gray-50 rounded-xl h-11"
              {...register("password", {
                required: "La contraseña es obligatoria",
                minLength: {
                  value: 8,
                  message: "La contraseña debe tener al menos 8 caracteres",
                },
              })}
              aria-invalid={!!errors.password}
            />
            {errors.password && (
              <FieldDescription>{errors.password?.message}</FieldDescription>
            )}
          </Field>

          <nav className="w-full flex flex-col gap-2 2xl:flex-row 2xl:justify-between pt-2">
            <Link
              className="text-gray-500 hover:text-gray-800 transition-colors block text-start text-sm"
              to={"/auth/register"}
            >
              ¿No tienes una cuenta?
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
            {isSubmitting ? "Iniciando..." : "Iniciar Sesión"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default Login;
