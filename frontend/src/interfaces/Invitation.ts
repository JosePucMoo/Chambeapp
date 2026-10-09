export interface InviteMemberDTO {
  email: string;
}

export interface InvitePreviewDTO {
  ownerName: string;
  projectTitle: string;
  inviteeEmail: string;
  status: string;
  expiresAt: string;
}

export interface AcceptInvitationDTO {
  projectId: string;
}
