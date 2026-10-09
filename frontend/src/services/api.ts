import axios, { AxiosError, type AxiosResponse } from "axios";
import type { ApiResponse } from "../interfaces/Api";
import type { ErrorResponse } from "../interfaces/Api";

const BASE_URL = import.meta.env.VITE_CHAMBEAPP_API_ORIGIN;

const apiClient = axios.create({
  baseURL: BASE_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response;
  },

  (error: AxiosError<ErrorResponse>) => {
    if (error.response?.data.detail && error.response.data.detail.length > 0) {
      const serverMessage = error.response.data.detail[0].message;

      return Promise.reject(new Error(serverMessage));
    }

    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/auth/login";
    }

    return Promise.reject(
      new Error(error.message || "Error de conexión con el servidor"),
    );
  },
);

export default apiClient;
