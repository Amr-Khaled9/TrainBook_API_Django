from time import timezone

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
    idempotency_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def can_transition_to(self, new_status):
        return new_status in self.ALLOWED_TRANSITIONS.get(self.status, [])

    def transition_to(self, new_status):
        if not self.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")

        self.status = new_status
        if new_status == self.Status.CONFIRMED:
            self.confirmed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email} - {self.seat}"