from django.db import models
from django.conf import settings
from trains.models import Seat


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    seat = models.OneToOneField(
        Seat,
        on_delete=models.PROTECT,
        related_name='booking'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email} - {self.seat}"