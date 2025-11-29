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
def other_user():
    return User.objects.create_user(
        email="other@user.com",
        password="123",
        is_verified=True
    )


@pytest.fixture
def user_task(user):
    return Task.objects.create(
        user=user,
        title="User Task",
        complete=False
    )


@pytest.fixture
def other_task(other_user):
    return Task.objects.create(
        user=other_user,
        title="Other Task",
        complete=False
    )


@pytest.mark.django_db
class TestTaskAPI:

    # -----------------------
    # Test Authentication
    # -----------------------
    def test_list_requires_auth(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    # -----------------------
    # Test List Tasks
    # -----------------------
    def test_list_user_tasks(self, api_client, user, user_task, other_task):
        url = reverse("todo:api-v1:task-list")
        api_client.force_login(user)

        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "User Task"

    # -----------------------
    # Test Create Task
    # -----------------------
    def test_create_task_unauthorized(self, api_client):
        url = reverse("todo:api-v1:task-list")
        data = {"title": "Test create"}

        response = api_client.post(url, data)

        assert response.status_code == 401

    def test_create_task_success(self, api_client, user):
        url = reverse("todo:api-v1:task-list")
        api_client.force_login(user)

        data = {"title": "New Task", "complete": False}
        response = api_client.post(url, data)

        assert response.status_code == 201
        assert Task.objects.filter(user=user).count() == 1

    def test_create_task_invalid_data(self, api_client, user):
        url = reverse("todo:api-v1:task-list")
        api_client.force_login(user)

        data = {"complete": True}  # title نیست
        response = api_client.post(url, data)

        assert response.status_code == 400

    # -----------------------
    # Test Retrieve Task
    # -----------------------
    def test_retrieve_own_task(self, api_client, user, user_task):
        api_client.force_login(user)
        url = reverse("todo:api-v1:task-detail", args=[user_task.id])

        response = api_client.get(url)

        assert response.status_code == 200
        assert "relative_url" not in response.data
        assert "absolute_url" not in response.data

    def test_retrieve_other_user_task(self, api_client, user, other_task):
        api_client.force_login(user)
        url = reverse("todo:api-v1:task-detail", args=[other_task.id])

        response = api_client.get(url)

        # باید 404 بده چون queryset فقط تسک‌های خود کاربر را برمی‌گرداند
        assert response.status_code == 404

    # -----------------------
    # Test Update Permissions
    # -----------------------
    def test_update_own_task(self, api_client, user, user_task):
        api_client.force_login(user)
        url = reverse("todo:api-v1:task-detail", args=[user_task.id])

        data = {"title": "Updated Title", "complete": True}
        response = api_client.patch(url, data)

        assert response.status_code == 200
        user_task.refresh_from_db()
        assert user_task.title == "Updated Title"

    def test_update_other_user_task_forbidden(self, api_client, user, other_task):
        api_client.force_login(user)
        url = reverse("todo:api-v1:task-detail", args=[other_task.id])

        response = api_client.patch(url, {"title": "Hack!"})

        # 404 چون در queryset نیست
        assert response.status_code == 404

    # -----------------------
    # Test Delete Task
    # -----------------------
    def test_delete_own_task(self, api_client, user, user_task):
        api_client.force_login(user)
        url = reverse("todo:api-v1:task-detail", args=[user_task.id])

        response = api_client.delete(url)

        assert response.status_code == 204
        assert Task.objects.count() == 0

    def test_delete_other_user_task(self, api_client, user, other_task):
        api_client.force_login(user)
        url = reverse("todo:api-v1:task-detail", args=[other_task.id])

        response = api_client.delete(url)

        assert response.status_code == 404

    # -----------------------
    # Test Filters, Search, Ordering
    # -----------------------
    def test_filter_by_complete(self, api_client, user):
        api_client.force_login(user)
        Task.objects.create(user=user, title="t1", complete=True)
        Task.objects.create(user=user, title="t2", complete=False)

        url = reverse("todo:api-v1:task-list") + "?complete=True"
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_search_title(self, api_client, user):
        api_client.force_login(user)
        Task.objects.create(user=user, title="Buy milk")
        Task.objects.create(user=user, title="Do homework")

        url = reverse("todo:api-v1:task-list") + "?search=milk"
        response = api_client.get(url)

        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "Buy milk"

    def test_ordering(self, api_client, user):
        api_client.force_login(user)
        Task.objects.create(user=user, title="A")
        Task.objects.create(user=user, title="B")

        url = reverse("todo:api-v1:task-list") + "?ordering=-created_date"
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 2
