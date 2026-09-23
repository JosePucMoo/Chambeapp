import apiClient from "./api";
import type {
  LoginResponse,
  RegisterPayload,
  ResetPasswordPayload,
} from "../interfaces/AuthResponse";
import type { ApiResponse } from "../interfaces/ApiResponse";

export const authService = {
  register: async (data: RegisterPayload) => {
    const response = await apiClient.post("/auth/register", data);
    return response.data;
  },

  login: async (email: string, password: string): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>("/auth/login", {
      email,
      password,
    });
    return response.data;
  },

  verifyEmail: async (
    token: string | undefined,
  ): Promise<ApiResponse<undefined>> => {
    const response = await apiClient.get(`/auth/verify-email/${token}`);
    return response.data;
  },

  forgotPassword: async (email: string) => {
    const response = await apiClient.post("/auth/forgot-password", { email });
    return response.data;
  },

  resetPassword: async (data: ResetPasswordPayload) => {
    const response = await apiClient.post("/auth/reset-password", data);
    return response.data;
  },
};
