from django.db import models


class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.source} → {self.destination})"


class Seat(models.Model):
    class SeatClass(models.TextChoices):
        ECONOMY = 'economy', 'Economy'
        BUSINESS = 'business', 'Business'
        FIRST = 'first', 'First Class'

    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name='seats'
    )
    seat_number = models.CharField(max_length=10)
    seat_class = models.CharField(
        max_length=20,
        choices=SeatClass.choices,
        default=SeatClass.ECONOMY
    )
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('train', 'seat_number')  # منع تكرار نفس رقم المقعد في نفس القطر

    def __str__(self):
        return f"Seat {self.seat_number} - {self.train.name}"