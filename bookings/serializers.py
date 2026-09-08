from rest_framework import serializers
from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    seat = serializers.IntegerField()
    idempotency_key = serializers.CharField(max_length=255, required=False, allow_blank=True)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'seat', 'status', 'idempotency_key', 'booked_at', 'confirmed_at')
        read_only_fields = ('user', 'status', 'booked_at', 'confirmed_at')