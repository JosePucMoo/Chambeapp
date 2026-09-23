import axios, { AxiosError, type AxiosResponse } from "axios";
import type { ApiResponse } from "../interfaces/ApiResponse";

const BASE_URL = import.meta.env.VITE_CHAMBEAPP_API_ORIGIN;

const apiClient = axios.create({
  baseURL: BASE_URL,
});

apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response;
  },

  (error: AxiosError<ApiResponse>) => {
    if (error.response?.data) {
      return Promise.reject(error.response.data);
    }

    const fallbackResponse: ApiResponse = {
      ok: false,
      message:
        error.message === "Network Error"
          ? "No hay conexión con el servidor."
          : "Ocurrió un error inesperado.",
    };

    return Promise.reject(fallbackResponse);
  },
);

export default apiClient;
