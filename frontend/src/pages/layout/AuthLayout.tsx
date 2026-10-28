import { Suspense } from "react";
import { Outlet } from "react-router-dom";
import logoImg from "@/assets/Logo.svg";

const AuthLayout = () => {
  return (
    <>
      <main className="flex min-h-screen items-center justify-center relative">
        <img
          src={logoImg}
          alt="App logo"
          className="inset-0 object-cover max-w-full h-auto absolute left-4 top-4"
        />
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
          <Outlet />
        </Suspense>
      </main>
    </>
  );
};

export default AuthLayout;
