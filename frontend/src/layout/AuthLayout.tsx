import { Outlet } from "react-router-dom";

const AuthLayout = () => {
  return (
    <>
      <main className="flex min-h-screen items-center justify-center relative">
        <img
          src="/src/assets/Logo.svg"
          alt="App logo"
          className="inset-0 object-cover w-1/5 h-auto absolute left-4 top-4"
        />
        <Outlet />
      </main>
    </>
  );
};

export default AuthLayout;
