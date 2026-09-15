import pytest
from django.utils import timezone
from datetime import timedelta
from bookings.factories import BookingFactory
from bookings.models import Booking
from bookings.tasks import expire_unpaid_bookings


@pytest.mark.django_db
def test_expire_unpaid_bookings_cancels_old_pending_bookings():
    old_time = timezone.now() - timedelta(minutes=15)
    booking = BookingFactory(status=Booking.Status.PENDING)
    # نعدل booked_at يدوي عشان نحاكي إنه اتعمل من 15 دقيقة
    Booking.objects.filter(id=booking.id).update(booked_at=old_time)

    expire_unpaid_bookings()

    booking.refresh_from_db()
    assert booking.status == Booking.Status.CANCELLED
    assert booking.seat.is_booked is False


@pytest.mark.django_db
def test_expire_unpaid_bookings_ignores_recent_bookings():
    booking = BookingFactory(status=Booking.Status.PENDING)  # اتعمل الآن

    expire_unpaid_bookings()

    booking.refresh_from_db()
    assert booking.status == Booking.Status.PENDING  # لسه معلق، متلغاش