from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework import status
from trains.models import Seat
from .models import Booking


class SeatAlreadyBookedError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This seat is already booked."
    default_code = "seat_already_booked"


class SeatNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Seat not found."
    default_code = "seat_not_found"


def create_booking(user, seat_id, idempotency_key=None):
    if idempotency_key:
        existing = Booking.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing
    with transaction.atomic():
        try:
            seat = Seat.objects.select_for_update().get(id=seat_id)
        except Seat.DoesNotExist:
            raise SeatNotFoundError()

        if seat.is_booked:
            raise SeatAlreadyBookedError()

        booking = Booking.objects.create(
            user=user,
            seat=seat,
            status=Booking.Status.PENDING
        )

        seat.is_booked = True
        seat.save()

        return booking