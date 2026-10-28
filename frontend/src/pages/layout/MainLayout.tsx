import { Suspense, useState } from "react";
import { Outlet } from "react-router-dom";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "./components/AppSidebar";
import { AppNavbar } from "./components/AppNavbar";
import type { LayoutContextType } from "@/interfaces/Context";

const MainLayout = () => {
  const [pageTitle, setPageTitle] = useState("Tablero");
  return (
    <SidebarProvider>
      <AppSidebar />

      <div className="flex flex-1 flex-col min-w-0 min-h-screen bg-gray-50/50">
        <AppNavbar title={pageTitle} />

        <main className="flex-1 overflow-y-auto bg-white">
          <Suspense
            fallback={
              <div
                role="status"
                aria-label="Cargando"
                className="flex min-h-40 items-center justify-center"
              >
                <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600" />
              </div>
            }
          >
            <Outlet context={{ setPageTitle } satisfies LayoutContextType} />
          </Suspense>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default MainLayout;
