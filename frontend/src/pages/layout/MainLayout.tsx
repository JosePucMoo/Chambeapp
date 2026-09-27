import { Outlet } from "react-router-dom";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "./components/AppSidebar";
import { AppNavbar } from "./components/AppNavbar";
import { useState } from "react";
import type { LayoutContextType } from "@/interfaces/Context";

const MainLayout = () => {
  const [pageTitle, setPageTitle] = useState("Tablero");
  return (
    <SidebarProvider>
      <AppSidebar />

      <div className="flex flex-1 flex-col min-w-0 min-h-screen bg-gray-50/50">
        <AppNavbar title={pageTitle} />

        <main className="flex-1 p-6 md:p-8 overflow-y-auto">
          <Outlet context={{ setPageTitle } satisfies LayoutContextType} />
        </main>
      </div>
    </SidebarProvider>
  );
};

export default MainLayout;
