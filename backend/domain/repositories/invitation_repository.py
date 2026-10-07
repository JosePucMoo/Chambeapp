from abc import ABC, abstractmethod

from domain.entities.project_invitation import InvitationPreview, ProjectInvitation


class InvitationRepository(ABC):
    @abstractmethod
    def get_by_token(self, token: str) -> InvitationPreview:
        pass

    @abstractmethod
    def create(self, project_invitation: ProjectInvitation) -> ProjectInvitation:
        pass

    @abstractmethod
    def has_alredy_been_sent_invitation(self, invitee_email: str, project_id: str) -> bool:
        pass
