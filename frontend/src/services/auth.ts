import type {
  ForgotPasswordRequest,
  LoginRequest,
  RegisterResponse,
  ResetPasswordRequest,
} from "../interfaces/Auth";
import apiClient from "./api";
import type { LoginResponse, RegisterRequest } from "../interfaces/Auth";
import type { ApiResponse } from "../interfaces/Api";
import type { User } from "@/interfaces/User";

export const authService = {
  register: async (
    data: RegisterRequest,
  ): Promise<ApiResponse<RegisterResponse>> => {
    const response = await apiClient.post("/auth/register", data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<ApiResponse<LoginResponse>> => {
    const response = await apiClient.post<ApiResponse<LoginResponse>>(
      "/auth/login",
      data,
    );
    return response.data;
  },

  verifyEmail: async (
    token: string | undefined,
  ): Promise<ApiResponse<undefined>> => {
    const response = await apiClient.get(`/auth/verify-email/${token}`);
    return response.data;
  },

  forgotPassword: async (
    data: ForgotPasswordRequest,
  ): Promise<ApiResponse<null>> => {
    const response = await apiClient.post("/auth/forgot-password", data);
    return response.data;
  },

  resetPassword: async (
    token: string,
    data: ResetPasswordRequest,
  ): Promise<ApiResponse<null>> => {
    const response = await apiClient.post(
      `/auth/reset-password/${token}`,
      data,
    );
    return response.data;
  },

  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    const response = await apiClient.get(`/auth/me`);
    return response.data;
  },
};
