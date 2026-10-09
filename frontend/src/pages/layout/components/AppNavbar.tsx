import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useAuth } from "@/hooks/useAuth";
import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface NavbarProps {
  title: string;
}

export function AppNavbar({ title }: NavbarProps) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/auth/login");
  };
  return (
    <header className="sticky top-0 z-10 flex h-16 w-full items-center justify-between border-b bg-white px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <SidebarTrigger className="hover:cursor-pointer" />
        <span className="h-4 w-px bg-gray-200" aria-hidden="true" />
        <h2 className="text-xl font-medium text-gray-700">{title}</h2>
      </div>

      <Popover>
        <PopoverTrigger
          render={
            <Button className="h-9 w-9 rounded-full hover:cursor-pointer bg-blue-500 text-white font-bold text-base">
              {user?.name.charAt(0).toUpperCase()}
            </Button>
          }
        />
        <PopoverContent className="w-auto mt-4 rounded-sm p-0">
          <Button
            variant="ghost"
            size="icon-lg"
            onClick={handleLogout}
            className="w-full h-full p-2 rounded-sm hover:cursor-pointer"
          >
            <LogOut className="h-5 w-5 mr-2" aria-label="Cerrar sesión" />
            Cerrar sesión
          </Button>
        </PopoverContent>
      </Popover>
    </header>
  );
}
