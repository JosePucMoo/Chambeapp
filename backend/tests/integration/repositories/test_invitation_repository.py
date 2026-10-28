from sqlalchemy.orm import Session

from infrastructure.repositories.invitation_repository_impl import InvitationRepositoryImpl
from domain.entities.project_invitation import ProjectInvitation
from domain.entities.enums import InvitationStatusEnum
from tests.integration.factories import Factories
from datetime import datetime, timedelta


class TestInvitationRepository:
    def test_create_and_get_by_id(self, db_session: Session):
        owner = Factories.create_user(db_session, email="inv_owner@test.com")
        project = Factories.create_project(db_session, owner_user=owner)
        repo = InvitationRepositoryImpl(db_session)
        inv = ProjectInvitation(
            invitee_email="invitee@test.com",
            status=InvitationStatusEnum.PENDING,
            project_id=project.id,
            invited_by=owner.id,
            token="tok-123",
            expires_at=datetime.now() + timedelta(days=1),
        )
        created = repo.create(inv)
        assert created.id is not None
        fetched = repo.get_by_token("tok-123")
        assert fetched is not None
        assert fetched.invitee_email == "invitee@test.com"

    def test_get_by_token(self, db_session: Session):
        owner = Factories.create_user(db_session, email="inv_owner2@test.com")
        project = Factories.create_project(db_session, owner_user=owner)
        repo = InvitationRepositoryImpl(db_session)
        inv = ProjectInvitation(
            invitee_email="invitee2@test.com",
            status=InvitationStatusEnum.PENDING,
            project_id=project.id,
            invited_by=owner.id,
            token="tok-456",
            expires_at=datetime.now() + timedelta(days=1),
        )
        repo.create(inv)
        fetched = repo.get_by_token("tok-456")
        assert fetched is not None

    def test_update_status(self, db_session: Session):
        owner = Factories.create_user(db_session, email="inv_owner3@test.com")
        project = Factories.create_project(db_session, owner_user=owner)
        repo = InvitationRepositoryImpl(db_session)
        inv = ProjectInvitation(
            invitee_email="invitee3@test.com",
            status=InvitationStatusEnum.PENDING,
            project_id=project.id,
            invited_by=owner.id,
            token="tok-789",
            expires_at=datetime.now() + timedelta(days=1),
        )
        repo.create(inv)
        updated = repo.update_status("tok-789", InvitationStatusEnum.ACCEPTED)
        assert updated.status == InvitationStatusEnum.ACCEPTED
