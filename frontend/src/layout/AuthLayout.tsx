import { Outlet } from "react-router-dom";

const AuthLayout = () => {
  return (
    <>
      <main className="container mx-auto flex min-h-screen items-center justify-center">
        <Outlet />
      </main>
    </>
  );
};

export default AuthLayout;
