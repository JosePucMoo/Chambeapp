import { Link, useLocation } from "react-router-dom";
import { LayoutGrid, ListPlus, PlusCircle, LogOut, Disc } from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupAction,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuBadge,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

import logoImg from "@/assets/Logo.svg";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

const projects = ["InterActive", "MyHotel", "MyAccounting", "InAct"];

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
              <SidebarMenuBadge className="text-sm font-bold right-3 pointer-events-none">
                2
              </SidebarMenuBadge>
            </SidebarMenuItem>

            <SidebarMenuItem>
              <SidebarMenuButton
                isActive={location.pathname === "/my-tasks"}
                className="hover:bg-blue-700 hover:text-white h-11 p-0"
              >
                <Link
                  to="/my-tasks"
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

        <Collapsible defaultOpen className="group/collapsible">
          <SidebarGroup>
            <SidebarGroupLabel
              className="text-blue-500 font-semibold text-base mb-2"
              render={<CollapsibleTrigger />}
            >
              Proyectos
            </SidebarGroupLabel>
            <SidebarGroupAction
              title="Add proyect"
              className="hover:bg-blue-50 mr-2"
            >
              <PlusCircle className="h-5 w-5  hover:text-blue-600" />
            </SidebarGroupAction>
            <CollapsibleContent>
              <SidebarGroupContent>
                <SidebarMenu className="space-y-1 mt-1">
                  {projects.map((project) => (
                    <SidebarMenuItem key={project}>
                      <SidebarMenuButton className=" hover:text-gray-700 hover:bg-gray-50 h-10 p-0">
                        <Link
                          to={`/proyectos/${project.toLowerCase()}`}
                          className="flex items-center gap-2 pl-3 w-full h-full"
                        >
                          <Disc className="h-3 w-3 fill-gray-100 stroke-gray-400" />
                          <span className="text-[15px]">{project}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroupContent>
            </CollapsibleContent>
          </SidebarGroup>
        </Collapsible>
      </SidebarContent>

      <SidebarFooter className="p-4 mb-2">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              className="hover:text-gray-800 hover:bg-gray-50 h-11"
              onClick={() => console.log("Cerrar sesión")}
            >
              <LogOut className="h-5 w-5 mr-1" />
              <span className="text-base font-medium">Logout</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
