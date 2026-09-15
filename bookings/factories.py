import factory
from accounts.factories import UserFactory
from trains.factories import SeatFactory
from .models import Booking


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    seat = factory.SubFactory(SeatFactory)
    status = Booking.Status.PENDING