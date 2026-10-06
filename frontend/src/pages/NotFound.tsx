import { ArrowLeft, FileQuestion, type LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

interface ResourceNotFoundProps {
  title?: string;
  description?: string;
  icon?: LucideIcon;
  backUrl?: string;
  backText?: string;
}

export const ResourceNotFound = ({
  title = "Recurso no encontrado",
  description = "Lo que estás buscando no existe o fue eliminado.",
  icon: Icon = FileQuestion, // Ícono por defecto
  backUrl = "/",
  backText = "Volver al inicio",
}: ResourceNotFoundProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-[70vh] w-full max-w-md mx-auto text-center space-y-4">
      <div className="p-4 bg-gray-100 rounded-full text-gray-400 mb-2">
        <Icon className="w-16 h-16" />
      </div>
      <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
      <p className="text-gray-500 text-sm">{description}</p>

      <div className="pt-4">
        <Button variant="default">
          <Link to={backUrl} className="flex items-center gap-2">
            <ArrowLeft className="w-4 h-4" />
            {backText}
          </Link>
        </Button>
      </div>
    </div>
  );
};
