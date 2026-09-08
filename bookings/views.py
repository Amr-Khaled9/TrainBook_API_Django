from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from .services import create_booking
from .tasks import send_booking_confirmation_email


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('seat', 'seat__train')

    def create(self, request, *args, **kwargs):
        input_serializer = BookingCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        booking = create_booking(
            user=request.user,
            seat_id=input_serializer.validated_data['seat'],
            idempotency_key=input_serializer.validated_data.get('idempotency_key')
        )

        output_serializer = BookingSerializer(booking)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        booking.transition_to(Booking.Status.CONFIRMED)
        send_booking_confirmation_email.delay(booking.id)
        return Response(BookingSerializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.transition_to(Booking.Status.CANCELLED)
        booking.seat.is_booked = False
        booking.seat.save()
        return Response(BookingSerializer(booking).data)