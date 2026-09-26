import { SidebarTrigger } from "@/components/ui/sidebar";

export function AppNavbar() {
  return (
    <header className="sticky top-0 z-10 flex h-16 w-full items-center justify-between border-b bg-white px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <SidebarTrigger />
        <span className="h-4 w-px bg-gray-200" aria-hidden="true" />
        <h2 className="text-sm font-medium text-gray-700">Panel Principal</h2>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 border-l pl-4">
          <div className="h-8 w-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold text-xs">
            U
          </div>
          <span className="text-sm font-medium text-gray-800 hidden md:inline-block">
            Usuario
          </span>
        </div>
      </div>
    </header>
  );
}
