import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Card,
  CardAction,
  CardContent,
  CardHeader,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/toast";
import { useAuth } from "@/hooks/useAuth";
import { invitationService } from "@/services/invitations";
import type { InvitePreviewDTO } from "@/interfaces/Invitation";

const ACCEPTED_STATUS = "Aceptada";

const AcceptInvitation = () => {
  const params = useParams();
  const token = params.token ?? "";
  const { user } = useAuth();
  const navigate = useNavigate();
  const [preview, setPreview] = useState<InvitePreviewDTO | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [isAccepting, setIsAccepting] = useState(false);

  useEffect(() => {
    const loadPreview = async () => {
      try {
        const response = await invitationService.getInvitationPreview(token);
        setPreview(response.data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error
            ? error.message
            : "No pudimos cargar la invitación.",
        );
      } finally {
        setIsLoading(false);
      }
    };
    void loadPreview();
  }, [token]);

  const handleLoginForAccept = () => {
    localStorage.setItem("pendingRedirect", `/invitations/${token}`);
  };

  const handleAccept = async () => {
    setIsAccepting(true);
    try {
      const response = await invitationService.acceptInvitation(token);
      toast.add({
        type: "success",
        title: "¡Invitación aceptada!",
        description: "Ya formas parte del proyecto.",
      });
      navigate(`/projects/${response.data?.projectId}`);
    } catch (error) {
      toast.add({
        type: "error",
        title: "No se pudo aceptar la invitación",
        description:
          error instanceof Error
            ? error.message
            : "Inténtalo de nuevo más tarde.",
      });
    } finally {
      setIsAccepting(false);
    }
  };

  if (isLoading) {
    return <p className="text-gray-500 font-medium">Cargando invitación...</p>;
  }

  if (errorMessage || !preview) {
    return (
      <Card className="w-full max-w-md ring-0 rounded-none px-6">
        <CardHeader className="mx-auto flex items-center justify-center h-20 w-20 rounded-full my-2 bg-red-100">
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
        </CardHeader>

        <CardContent className="space-y-2">
          <h2 className="text-2xl font-bold text-gray-900 text-center">
            {errorMessage || "Invitación no válida"}
          </h2>
          <p className="text-gray-500 mb-4 text-center">
            Esta invitación no existe o ya expiró. Solicita una nueva a quien te
            invitó.
          </p>
        </CardContent>

        <CardAction className="w-full">
          <Link
            to="/auth/login"
            className="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-xl text-sm font-bold text-white bg-blue-500 hover:bg-blue-700 focus:outline-none transition-colors"
          >
            Ir a iniciar sesión
          </Link>
        </CardAction>
      </Card>
    );
  }

  if (preview.status === ACCEPTED_STATUS) {
    return (
      <Card className="w-full max-w-md ring-0 rounded-none px-6">
        <CardHeader className="mx-auto flex items-center justify-center h-20 w-20 rounded-full my-2 bg-green-100">
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
        </CardHeader>

        <CardContent className="space-y-2">
          <h2 className="text-2xl font-bold text-gray-900 text-center">
            Invitación aceptada
          </h2>
          <p className="text-gray-500 mb-4 text-center">
            Ya formas parte del proyecto{" "}
            <span className="font-semibold text-gray-700">
              {preview.projectTitle}
            </span>
            .
          </p>
        </CardContent>

        <CardAction className="w-full">
          {user ? (
            <Button
              onClick={handleAccept}
              disabled={isAccepting}
              className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold h-12 uppercase"
            >
              {isAccepting ? "Cargando..." : "Ir al tablero"}
            </Button>
          ) : (
            <Link
              to="/auth/login"
              onClick={handleLoginForAccept}
              className="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-xl text-sm font-bold text-white bg-blue-500 hover:bg-blue-700 focus:outline-none transition-colors"
            >
              Ir a iniciar sesión
            </Link>
          )}
        </CardAction>
      </Card>
    );
  }

  if (!user) {
    return (
      <Card className="w-full max-w-md ring-0 rounded-none px-6">
        <CardHeader className="mx-auto flex items-center justify-center h-20 w-20 rounded-full my-2 bg-blue-100">
          <svg
            className="h-10 w-10 text-blue-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </CardHeader>

        <CardContent className="space-y-2">
          <h2 className="text-2xl font-bold text-gray-900 text-center">
            Inicia sesión para aceptar
          </h2>
          <p className="text-gray-500 mb-4 text-center">
            {preview.ownerName} te invitó a colaborar en el proyecto{" "}
            <span className="font-semibold text-gray-700">
              {preview.projectTitle}
            </span>
            .
          </p>
        </CardContent>

        <CardAction className="w-full">
          <Link
            to="/auth/login"
            onClick={handleLoginForAccept}
            className="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-xl text-sm font-bold text-white bg-blue-500 hover:bg-blue-700 focus:outline-none transition-colors"
          >
            Iniciar sesión
          </Link>
        </CardAction>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md ring-0 rounded-none px-6">
      <CardHeader className="mx-auto flex items-center justify-center h-20 w-20 rounded-full my-2 bg-green-100">
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
            d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
          />
        </svg>
      </CardHeader>

      <CardContent className="space-y-2 text-center">
        <h2 className="text-2xl font-bold text-gray-900">
          Invitación al tablero
        </h2>
        <p className="text-gray-500 mb-4">
          {preview.ownerName} te invitó a colaborar en el proyecto{" "}
          <span className="font-semibold text-gray-700">
            {preview.projectTitle}
          </span>
          .
        </p>
        <p className="text-xs text-gray-400">
          La invitación fue enviada a {preview.inviteeEmail}.
        </p>
      </CardContent>

      <CardAction className="w-full">
        <Button
          onClick={handleAccept}
          disabled={isAccepting}
          className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold h-12 uppercase"
        >
          {isAccepting ? "Aceptando..." : "Aceptar invitación"}
        </Button>
      </CardAction>
    </Card>
  );
};

export default AcceptInvitation;
