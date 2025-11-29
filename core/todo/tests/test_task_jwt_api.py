import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from todo.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="admin@admin.com",
        password="123",
        is_verified=True
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
class TestTaskAPI:

    # -------------------------
    # JWT Authentication
    # -------------------------
    def test_jwt_authentication(self, api_client, user):
        url = reverse("accounts:api-v1:jwt-create")
        response = api_client.post(url, {"email": "admin@admin.com", "password": "123"})
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    # -------------------------
    # List (Requires Auth)
    # -------------------------
    def test_task_list_requires_auth(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_task_list_authenticated(self, auth_client):
        url = reverse("todo:api-v1:task-list")
        response = auth_client.get(url)
        assert response.status_code == 200

    # -------------------------
    # Create Task
    # -------------------------
    def test_create_task(self, auth_client):
        url = reverse("todo:api-v1:task-list")
        data = {"title": "My Task", "complete": False}
        response = auth_client.post(url, data)
        assert response.status_code == 201
        assert response.data["title"] == "My Task"

    # -------------------------
    # Invalid Create
    # -------------------------
    def test_create_invalid_task(self, auth_client):
        url = reverse("todo:api-v1:task-list")
        response = auth_client.post(url, {"complete": True})
        assert response.status_code == 400

    # -------------------------
    # Retrieve Detail
    # -------------------------
    def test_get_task_detail(self, auth_client, user):
        task = Task.objects.create(user=user, title="Detail Test")
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": task.id})
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data["title"] == "Detail Test"

    # -------------------------
    # Update / Owner Only
    # -------------------------
    def test_update_only_owner(self, api_client, user):
        t1 = Task.objects.create(user=user, title="To Update")

        another_user = User.objects.create_user(
            email="other@admin.com", password="123", is_verified=True
        )
        api_client.force_authenticate(user=another_user)

        url = reverse("todo:api-v1:task-detail", kwargs={"pk": t1.id})
        response = api_client.put(url, {"title": "Hack", "complete": False})

        assert response.status_code == 404  # Permission denied

    # -------------------------
    # Filter ?complete=true
    # -------------------------
    def test_filter_by_complete(self, auth_client, user):
        Task.objects.create(user=user, title="task 1", complete=True)
        Task.objects.create(user=user, title="task 2", complete=False)

        url = reverse("todo:api-v1:task-list") + "?complete=True"
        response = auth_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    # -------------------------
    # Search ?search=keyword
    # -------------------------
    def test_search_title(self, auth_client, user):
        Task.objects.create(user=user, title="hello world")
        Task.objects.create(user=user, title="python test")

        url = reverse("todo:api-v1:task-list") + "?search=python"
        response = auth_client.get(url)

        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "python test"

    # -------------------------
    # Ordering ?ordering=created_date
    # -------------------------
    def test_ordering(self, auth_client, user):
        Task.objects.create(user=user, title="A")
        Task.objects.create(user=user, title="B")

        url = reverse("todo:api-v1:task-list") + "?ordering=created_date"
        response = auth_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 2

    # -------------------------
    # Pagination
    # -------------------------
    def test_pagination(self, auth_client, user):
        for i in range(25):
            Task.objects.create(user=user, title=f"Task {i}")

        url = reverse("todo:api-v1:task-list")
        response = auth_client.get(url)

        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) <= 20  # LargeResultsSetPagination (page_size=20)

