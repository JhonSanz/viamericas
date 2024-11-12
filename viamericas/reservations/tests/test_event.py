import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Permission
from reservations.models import Event, Category, Speaker
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_with_permissions(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    user.is_staff = True
    user.save()

    token, _ = Token.objects.get_or_create(user=user)

    view_permission = Permission.objects.get(codename="view_event")
    add_permission = Permission.objects.get(codename="add_event")
    user.user_permissions.add(view_permission, add_permission)

    return user, token


@pytest.fixture
def sample_category(db):
    return Category.objects.create(
        name="Sample Category", description="A test category"
    )


@pytest.fixture
def sample_speaker(db):
    return Speaker.objects.create(
        first_name="John",
        last_name="Doe",
        bio="Test speaker",
        email="johndoe@example.com",
    )


@pytest.fixture
def sample_event(db, sample_category, sample_speaker):
    event = Event.objects.create(
        name="Sample Event",
        description="This is a sample event.",
        date=timezone.now(),
        location="Sample Location",
        category=sample_category,
    )
    event.speakers.add(sample_speaker)
    return event


@pytest.mark.django_db
def test_event_list_without_filters(api_client, user_with_permissions, sample_event):
    user, token = user_with_permissions
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    response = api_client.get("/events/")
    assert response.status_code == 200
    assert len(response.data["results"]) > 0


@pytest.mark.django_db
def test_event_list_with_name_filter(api_client, user_with_permissions, sample_event):
    user, token = user_with_permissions
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    response = api_client.get(f"/events/?name=Sample")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == "Sample Event"


@pytest.mark.django_db
def test_event_creation(api_client, user_with_permissions, sample_event):
    user, token = user_with_permissions
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    data = {
        "name": "New Event",
        "date": timezone.now().isoformat(),
        "category": 1,
        "description": "test",
        "location": "test",
        "speakers": [1],
    }

    response = api_client.post("/events/", data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "New Event"


@pytest.mark.django_db
def test_event_list_with_date_filter(api_client, user_with_permissions, sample_event):
    user, token = user_with_permissions
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    date_from = (timezone.now() - timezone.timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    date_to = (timezone.now() + timezone.timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    response = api_client.get(f"/events/?date_from={date_from}&date_to={date_to}")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == "Sample Event"
