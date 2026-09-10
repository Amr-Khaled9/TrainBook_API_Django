from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from trains.utils import broadcast_seat_update

@shared_task
def expire_unpaid_bookings():
    from .models import Booking

    expiry_threshold = timezone.now() - timedelta(minutes=10)
    expired_bookings = Booking.objects.filter(
        status=Booking.Status.PENDING,
        booked_at__lt=expiry_threshold
    ).select_related('seat')

    count = 0
    for booking in expired_bookings:
        booking.transition_to(Booking.Status.CANCELLED)
        booking.seat.is_booked = False
        booking.seat.save()
        broadcast_seat_update(booking.seat)
        count += 1

    return f"Expired {count} bookings"


@shared_task
def send_booking_confirmation_email(booking_id):
    from .models import Booking
    from django.core.mail import send_mail

    try:
        booking = Booking.objects.select_related('user', 'seat', 'seat__train').get(id=booking_id)
    except Booking.DoesNotExist:
        return "Booking not found"

    send_mail(
        subject="Booking Confirmed - TrainBook",
        message=(
            f"Your booking for seat {booking.seat.seat_number} "
            f"on {booking.seat.train.name} is confirmed."
        ),
        from_email="noreply@trainbook.com",
        recipient_list=[booking.user.email],
        fail_silently=False,
    )
    return f"Confirmation email sent for booking {booking_id}"