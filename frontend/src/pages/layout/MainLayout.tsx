import { Outlet } from "react-router-dom";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "./components/AppSidebar";
import { AppNavbar } from "./components/AppNavbar";

const MainLayout = () => {
  return (
    <SidebarProvider>
      <AppSidebar />

      <div className="flex flex-1 flex-col min-w-0 min-h-screen bg-gray-50/50">
        <AppNavbar />

        <main className="flex-1 p-6 md:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </SidebarProvider>
  );
};

export default MainLayout;
