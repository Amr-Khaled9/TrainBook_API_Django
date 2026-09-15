import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.factories import UserFactory
from bookings.factories import BookingFactory


def get_auth_client(user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client


@pytest.mark.django_db
def test_user_cannot_see_other_users_bookings():
    user_a = UserFactory()
    user_b = UserFactory()
    booking_a = BookingFactory(user=user_a)
    booking_b = BookingFactory(user=user_b)

    client = get_auth_client(user_a)
    response = client.get('/api/bookings/')

    booking_ids = [b['id'] for b in response.data['results']]
    assert booking_a.id in booking_ids
    assert booking_b.id not in booking_ids


@pytest.mark.django_db
def test_user_cannot_confirm_another_users_booking():
    user_a = UserFactory()
    user_b = UserFactory()
    booking_b = BookingFactory(user=user_b)

    client = get_auth_client(user_a)
    response = client.post(f'/api/bookings/{booking_b.id}/confirm/')

    assert response.status_code == 404  # مايشوفهاش أصلاً، مش حتى 403


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_bookings():
    client = APIClient()
    response = client.get('/api/bookings/')
    assert response.status_code == 401