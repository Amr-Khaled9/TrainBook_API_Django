from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'seat', 'status', 'booked_at', 'confirmed_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'seat__seat_number')
    readonly_fields = ('booked_at',)