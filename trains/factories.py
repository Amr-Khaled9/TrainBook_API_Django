import factory
from django.utils import timezone
from datetime import timedelta
from .models import Train, Seat


class TrainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Train

    name = factory.Sequence(lambda n: f'Train {n}')
    source = 'Cairo'
    destination = 'Alexandria'
    departure_time = factory.LazyFunction(lambda: timezone.now() + timedelta(days=1))
    arrival_time = factory.LazyFunction(lambda: timezone.now() + timedelta(days=1, hours=3))
    price = 150.00


class SeatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seat

    train = factory.SubFactory(TrainFactory)
    seat_number = factory.Sequence(lambda n: f'A{n}')
    seat_class = Seat.SeatClass.ECONOMY
    is_booked = False