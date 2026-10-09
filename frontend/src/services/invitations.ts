import type { ApiResponse } from "@/interfaces/Api";
import apiClient from "./api";
import type {
  AcceptInvitationDTO,
  InvitePreviewDTO,
} from "@/interfaces/Invitation";

export const invitationService = {
  getInvitationPreview: async (
    token: string,
  ): Promise<ApiResponse<InvitePreviewDTO>> => {
    const response = await apiClient.get(`/invitations/${token}`);
    return response.data;
  },

  acceptInvitation: async (
    token: string,
  ): Promise<ApiResponse<AcceptInvitationDTO>> => {
    const response = await apiClient.post(`/invitations/${token}/accept`);
    return response.data;
  },
};
