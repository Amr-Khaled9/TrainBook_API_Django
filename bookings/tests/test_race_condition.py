import threading
import pytest
from django.db import connection
from trains.factories import SeatFactory
from accounts.factories import UserFactory
from bookings.services import create_booking, SeatAlreadyBookedError
from bookings.models import Booking


@pytest.mark.django_db(transaction=True)
def test_double_booking_prevented_by_select_for_update():
    seat = SeatFactory()
    user_a = UserFactory()
    user_b = UserFactory()

    results = {'success': 0, 'failed': 0}

    def attempt_booking(user):
        try:
            create_booking(user=user, seat_id=seat.id)
            results['success'] += 1
        except SeatAlreadyBookedError:
            results['failed'] += 1
        finally:
            connection.close()  # كل thread لازم تقفل الاتصال بتاعها بالداتابيز

    thread_a = threading.Thread(target=attempt_booking, args=(user_a,))
    thread_b = threading.Thread(target=attempt_booking, args=(user_b,))

    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()

    assert results['success'] == 1
    assert results['failed'] == 1
    assert Booking.objects.filter(seat=seat).count() == 1