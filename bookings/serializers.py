from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'seat', 'status', 'booked_at', 'confirmed_at')
        read_only_fields = ('user', 'status', 'booked_at', 'confirmed_at')