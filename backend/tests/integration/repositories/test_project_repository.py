from datetime import date

from domain.entities.enums import RoleEnum
from infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from infrastructure.repositories.user_project_link_repository_impl import (
    UserProjectLinkRepositoryImpl,
)
from tests.integration.factories import Factories


class TestProjectRepository:
    def test_create_and_get_by_id(self, db_session):
        owner = Factories.create_user(db_session, name="Owner", email="owner@test.com")
        project = Factories.create_project(db_session, owner_user=owner, title="Chambeapp")

        repo = ProjectRepositoryImpl(db_session)
        fetched = repo.get_by_id(project.id)

        assert fetched is not None
        assert fetched.title == "Chambeapp"
        assert fetched.client == "Cliente"

    def test_update_project(self, db_session):
        owner = Factories.create_user(db_session, name="Owner", email="owner@test.com")
        project = Factories.create_project(db_session, owner_user=owner)

        project.title = "Updated"
        project.client = "NewClient"
        delivery = date(2027, 1, 15)
        project.delivery_date = delivery

        repo = ProjectRepositoryImpl(db_session)
        updated = repo.update(project)

        assert updated.title == "Updated"
        assert updated.client == "NewClient"
        assert updated.delivery_date == delivery

    def test_get_project_members(self, db_session):
        owner = Factories.create_user(db_session, name="Owner", email="owner@test.com")
        member = Factories.create_user(db_session, name="Member", email="member@test.com")
        project = Factories.create_project(db_session, owner_user=owner)

        link_repo = UserProjectLinkRepositoryImpl(db_session)
        from domain.entities.user_project_link import UserProjectLink

        link = UserProjectLink(role=RoleEnum.GUEST, user_id=member.id, project_id=project.id)
        link_repo.create(link)

        repo = ProjectRepositoryImpl(db_session)
        members = repo.get_project_members(project.id)

        assert len(members) == 2
        emails = {m.email for m in members}
        assert "owner@test.com" in emails
        assert "member@test.com" in emails

    def test_execute_paginated_summary_basic(self, db_session):
        owner = Factories.create_user(db_session, name="Owner", email="owner@test.com")
        project = Factories.create_project(db_session, owner_user=owner, title="P1")
        columns = Factories.create_default_columns(db_session, project)
        Factories.create_task(db_session, columns[0], owner)
        Factories.create_task(db_session, columns[2], owner)

        repo = ProjectRepositoryImpl(db_session)
        total_count, summaries = repo.get_paginated_dashboard_projects(
            user_id=owner.id, page=1, page_size=10
        )

        assert total_count == 1
        assert len(summaries) == 1
        assert summaries[0].title == "P1"

    def test_execute_paginated_summary_filters_by_search(self, db_session):
        owner = Factories.create_user(db_session, name="Owner", email="owner@test.com")
        project1 = Factories.create_project(db_session, owner_user=owner, title="Alfa")
        project2 = Factories.create_project(db_session, owner_user=owner, title="Beta")
        Factories.create_default_columns(db_session, project1)
        Factories.create_default_columns(db_session, project2)

        repo = ProjectRepositoryImpl(db_session)
        from domain.entities.project import ProjectFilters

        total_count, summaries = repo.get_paginated_dashboard_projects(
            user_id=owner.id, page=1, page_size=10, filters=ProjectFilters(search="Alf")
        )
        assert total_count == 1
        assert summaries[0].title == "Alfa"

    def test_execute_paginated_summary_empty(self, db_session):
        owner = Factories.create_user(db_session, name="Owner", email="owner@test.com")
        repo = ProjectRepositoryImpl(db_session)
        total_count, summaries = repo.get_paginated_dashboard_projects(
            user_id=owner.id, page=1, page_size=10
        )
        assert total_count == 0
        assert summaries == []
