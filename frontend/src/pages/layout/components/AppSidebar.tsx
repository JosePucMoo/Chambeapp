import { Link, useLocation } from "react-router-dom";
import { LayoutGrid, ListPlus, FolderKanban, LogOut } from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

import logoImg from "@/assets/Logo.svg";

export function AppSidebar() {
  const location = useLocation();
  return (
    <Sidebar className="border-r border-gray-100">
      <SidebarHeader className="p-6">
        <img src={logoImg} alt="App logo sidebar" className="max-w-full" />
      </SidebarHeader>

      <SidebarContent className="px-3">
        <SidebarGroup>
          <SidebarMenu className="space-y-1">
            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={location.pathname === "/"}
                className=" hover:bg-blue-700 hover:text-white h-11 p-0"
              >
                <Link
                  to="/"
                  className="flex items-center gap-2 pl-3 w-full h-full"
                >
                  <LayoutGrid className="w-5 h-5" />
                  <span className="text-base font-medium">Tablero</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={location.pathname === "/projects"}
                className=" hover:bg-blue-700 hover:text-white h-11 p-0"
              >
                <Link
                  to="/projects"
                  className="flex items-center gap-2 pl-3 w-full h-full"
                >
                  <FolderKanban className="w-5 h-5" />
                  <span className="text-base font-medium">Proyectos</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={location.pathname === "/tasks"}
                className="hover:bg-blue-700 hover:text-white h-11 p-0"
              >
                <Link
                  to="/tasks"
                  className="flex items-center gap-2 pl-3 w-full h-full"
                >
                  <ListPlus className="w-5 h-5" />
                  <span className="text-base font-medium">Mis tareas</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroup>

        <div className="px-4 py-3">
          <hr className="border-gray-200" />
        </div>
      </SidebarContent>

      <SidebarFooter className="p-4 mb-2">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              className="hover:text-gray-800 hover:bg-gray-50 h-11"
              onClick={() => console.log("Cerrar sesión")}
            >
              <LogOut className="h-5 w-5 mr-1" />
              <span className="text-base font-medium">Cerrar sesión</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
