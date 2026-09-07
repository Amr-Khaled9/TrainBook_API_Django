from rest_framework import serializers
from .models import Train, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ('id', 'train', 'seat_number', 'seat_class', 'is_booked')
        read_only_fields = ('is_booked',) 


class TrainSerializer(serializers.ModelSerializer):
    available_seats_count = serializers.SerializerMethodField()

    class Meta:
        model = Train
        fields = (
            'id', 'name', 'source', 'destination',
            'departure_time', 'arrival_time', 'price',
            'available_seats_count', 'created_at'
        )

    def get_available_seats_count(self, obj):
        return obj.seats.filter(is_booked=False).count()


class TrainDetailSerializer(TrainSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta(TrainSerializer.Meta):
        fields = TrainSerializer.Meta.fields + ('seats',)