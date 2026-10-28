from infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from infrastructure.repositories.user_project_link_repository_impl import (
    UserProjectLinkRepositoryImpl,
)
from domain.entities.user_project_link import UserProjectLink
from domain.entities.enums import RoleEnum
from tests.integration.factories import Factories


class TestUserProjectLinkRepository:
    def test_create_and_get_by_user_and_project(self, db_session):
        owner = Factories.create_user(db_session, email="owner1@test.com")
        member = Factories.create_user(db_session, email="member1@test.com")
        project = Factories.create_project(db_session, owner_user=owner)

        link_repo = UserProjectLinkRepositoryImpl(db_session)
        link = UserProjectLink(role=RoleEnum.GUEST, user_id=member.id, project_id=project.id)
        created = link_repo.create(link)
        assert created.id is not None

        fetched = link_repo.get_by_user_and_project(user_id=member.id, project_id=project.id)
        assert fetched is not None
        assert fetched.role == RoleEnum.GUEST

    def test_get_members_by_project(self, db_session):
        owner = Factories.create_user(db_session, email="owner2@test.com")
        member = Factories.create_user(db_session, email="member2@test.com")
        project = Factories.create_project(db_session, owner_user=owner)

        link_repo = UserProjectLinkRepositoryImpl(db_session)
        link = UserProjectLink(role=RoleEnum.GUEST, user_id=member.id, project_id=project.id)
        link_repo.create(link)

        proj_repo = ProjectRepositoryImpl(db_session)
        members = proj_repo.get_project_members(project.id)
        assert len(members) >= 2
