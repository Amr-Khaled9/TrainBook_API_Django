from django.contrib import admin
from .models import Train, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 1


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'destination', 'departure_time', 'price')
    list_filter = ('source', 'destination')
    search_fields = ('name', 'source', 'destination')
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'train', 'seat_class', 'is_booked')
    list_filter = ('seat_class', 'is_booked', 'train')
    search_fields = ('seat_number',)