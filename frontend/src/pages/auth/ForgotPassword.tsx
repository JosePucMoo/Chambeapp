import { Link } from "react-router-dom";

const ForgotPassword = () => {
  return (
    <div className="flex sm:shadow-2xl overflow-hidden w-full sm:w-6/12 xl:w-4/12 items-center justify-center px-10 md:px-15 relative">
      <img
        src="/src/assets/Logo.svg"
        className="inset-0  object-cover w-1/4 absolute left-4 top-4"
      />
      <div className="flex-col w-full py-10">
        <h1 className="block text-center text-gray-700 text-5xl font-semibold mt-5">
          Recupera tu <span className="text-blue-500 font-bold">acceso</span>
        </h1>
        <form className="mt-5">
          <div className="my-5">
            <label className="block text-md font-medium text-gray-700">
              Correo Electrónico
            </label>
            <input
              type="email"
              placeholder="correo@correo.com"
              className="border border-gray-300 w-full p-2 mt-2 bg-gray-50 rounded-xl"
            />
          </div>

          <nav className="w-full flex flex-col gap-1 2xl:flex-row 2xl:justify-between">
            <Link className="text-gray-500 block text-start text-sm" to={"/"}>
              ¿Ya tienes una cuenta?
            </Link>
            <Link
              className="text-gray-500 block text-start text-sm"
              to={"/forgot-password"}
            >
              ¿No tienes una cuenta?
            </Link>
          </nav>

          <input
            className="mt-10 uppercase bg-blue-500 rounded-xs hover:bg-blue-700 text-white w-full text-base font-bold py-3"
            value="Enviar Instrucciones"
            type="submit"
          />
        </form>
      </div>
    </div>
  );
};

export default ForgotPassword;
