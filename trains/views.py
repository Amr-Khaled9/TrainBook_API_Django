from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Train, Seat
from .serializers import TrainSerializer, TrainDetailSerializer, SeatSerializer
from .filters import TrainFilter


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all().order_by('departure_time')
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TrainFilter
    search_fields = ('name', 'source', 'destination')
    ordering_fields = ('departure_time', 'price')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TrainDetailSerializer
        return TrainSerializer

    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        train = self.get_object()
        seats = train.seats.filter(is_booked=False)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.select_related('train').all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ('train', 'seat_class', 'is_booked')