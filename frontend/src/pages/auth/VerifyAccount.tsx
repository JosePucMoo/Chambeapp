import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { authService } from "../../services/auth";
import {
  Card,
  CardAction,
  CardContent,
  CardHeader,
} from "@/components/ui/card";

const VerifyAccount = () => {
  const [confirmedAccount, setConfirmedAccount] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [message, setMessage] = useState("");
  const params = useParams();

  const { token } = params;

  useEffect(() => {
    const confirmAccount = async () => {
      try {
        const response = await authService.verifyEmail(token);
        setConfirmedAccount(true);
        setMessage(response.message);
      } catch (err: any) {
        setMessage(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    confirmAccount();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <p className="text-gray-500 font-medium">Verificando tu correo...</p>
      </div>
    );
  }

  return (
    <Card className="w-full max-w-md sm:shadow-2xl ring-0 rounded-none px-6 ">
      <CardHeader
        className={`mx-auto flex items-center justify-center h-20 w-20 rounded-full my-2 ${
          confirmedAccount ? "bg-green-100" : "bg-red-100"
        }`}
      >
        {confirmedAccount ? (
          <svg
            className="h-10 w-10 text-green-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        ) : (
          <svg
            className="h-10 w-10 text-red-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        )}
      </CardHeader>

      <CardContent className="space-y-2">
        <h2 className="text-2xl font-bold text-gray-900 text-center">
          {message}
        </h2>

        <p className="text-gray-500 mb-4">
          {confirmedAccount
            ? "Tu cuenta ha sido confirmada correctamente. Ya puedes acceder a tus tableros en Chambeapp."
            : "Por razones de seguridad, los enlaces de verificación solo pueden usarse una vez."}
        </p>
      </CardContent>

      <CardAction className="w-full">
        {confirmedAccount ? (
          <Link
            to="/auth/login"
            className="w-full flex justify-center uppercase py-3 px-4 border border-transparent shadow-sm text-sm font-bold text-white bg-blue-500 hover:bg-blue-700 focus:outline-none transition-colors"
          >
            Ir a Iniciar Sesión
          </Link>
        ) : (
          <>
            <Link
              to="/auth/login"
              className="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-xl text-sm font-bold text-white bg-blue-500 hover:bg-blue-700 focus:outline-none transition-colors"
            >
              Volver al inicio de sesión
            </Link>
          </>
        )}
      </CardAction>
    </Card>
  );
};

export default VerifyAccount;
