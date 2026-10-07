from fastapi import APIRouter, HTTPException, status

from application.use_cases.project.invite_member import InviteMemberUseCase
from application.use_cases.project.get_invitation import GetInvitationUseCase
from application.use_cases.project.accept_invitation import AcceptInvitationUseCase
from domain.utils.constants import Constants
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_expired_exception import ResourceExpiredException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.invitation_schema import (
    InviteMemberDTO,
    InvitePreviewDTO,
    AcceptInvitationDTO,
)
from infrastructure.api.dependencies import (
    CurrentUser,
    EmailSenderDep,
    InvitationRepositoryDep,
    ProjectRepositoryDep,
    UserProjectLinkRepositoryDep,
    UserRepositoryDep,
)

router = APIRouter(prefix="/invitations", tags=["Invitations"])


@router.post(
    path="/project/{project_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[None],
)
def send_invitation(
    project_id: str,
    inviteMemberDTO: InviteMemberDTO,
    current_user: CurrentUser,
    repository: InvitationRepositoryDep,
    project_repository: ProjectRepositoryDep,
    user_repository: UserRepositoryDep,
    user_project_link_repository: UserProjectLinkRepositoryDep,
    email_sender: EmailSenderDep,
):
    try:
        use_case = InviteMemberUseCase(
            repository=repository,
            project_repository=project_repository,
            user_repository=user_repository,
            user_project_link_repository=user_project_link_repository,
            email_sender=email_sender,
        )
        use_case.execute(
            current_user=current_user, project_id=project_id, invitee_email=inviteMemberDTO.email
        )

        return ApiResponse(ok=True, message=Constants.INVITATION_ACCEPTED, data=None)
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ResourceAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    path="/{token}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[InvitePreviewDTO],
)
def get_invitation_by_token(
    token: str,
    repository: InvitationRepositoryDep,
):
    try:
        use_case = GetInvitationUseCase(
            repository=repository,
        )
        invitation = use_case.execute(token=token)
        data = InvitePreviewDTO.model_validate(invitation)

        return ApiResponse(ok=True, message=Constants.INVITATION_ACCEPTED, data=data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ResourceExpiredException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    path="/{token}/accept",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[AcceptInvitationDTO],
)
def accept_invitation(
    token: str,
    current_user: CurrentUser,
    repository: InvitationRepositoryDep,
    user_project_link_repository: UserProjectLinkRepositoryDep,
):
    try:
        use_case = AcceptInvitationUseCase(
            repository=repository, user_project_link_repository=user_project_link_repository
        )
        project_id = use_case.execute(token=token, current_user=current_user)
        data = AcceptInvitationDTO(project_id=project_id)

        return ApiResponse(ok=True, message=Constants.INVITATION_ACCEPTED, data=data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ResourceExpiredException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
