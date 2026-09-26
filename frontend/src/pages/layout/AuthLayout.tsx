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
        <Outlet />
      </main>
    </>
  );
};

export default AuthLayout;
