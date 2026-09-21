import { Link } from "react-router-dom";

const VerifyAccount = () => {
  return (
    <div className="flex sm:shadow-2xl overflow-hidden w-full sm:w-6/12 xl:w-4/12 items-center justify-center px-10 md:px-15 relative">
      <img
        src="/src/assets/Logo.svg"
        className="inset-0  object-cover w-1/4 absolute left-4 top-4"
      />
      <div className="flex-col w-full py-10">
        <h1 className="block text-center text-blue-500 text-5xl font-semibold mt-5">
          Cuenta confirmada{" "}
          <span className="text-black font-bold">exitosamente</span>
        </h1>
        <form className="mt-5">
          <nav className="w-full flex justify-center">
            <Link className="text-gray-500 block text-sm" to={"/"}>
              Iniciar Sesión
            </Link>
          </nav>
        </form>
      </div>
    </div>
  );
};

export default VerifyAccount;
