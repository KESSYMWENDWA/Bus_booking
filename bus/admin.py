from django.contrib import admin
from .models import Bus, Booking, Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus', 'from_location', 'to_location', 'date', 'seat_number', 'created_at')
    list_filter = ('bus', 'date')  # Filters for the admin list view
    search_fields = ('from_location', 'to_location', 'seat_number')  # Fields to search in admin interface


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'bus_name', 'payment_method', 'price', 'created_at')
    search_fields = ('booking_busname', 'payment_method', 'booking_seat_number')
    list_filter = ('payment_method', 'created_at')
admin.site.register(Payment, PaymentAdmin),
admin.site.register(Bus)

