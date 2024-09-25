from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    route = models.CharField(max_length=100)
    hours_of_travel = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bus_images/')
    no_of_passengers = models.PositiveIntegerField()  # Total number of seats

    def _str_(self):
        return self.name
    

class UserSignUp(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def str(self):
        return self.username

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Link to User
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bookings')
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateField()
    seat_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('bus', 'date', 'seat_number')

    def _str_(self):
        return f"Booking for {self.bus.name} - Seat {self.seat_number} on {self.date}"
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link payment to the user
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=100)
    route = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_number = models.IntegerField()
    payment_method = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_date = models.CharField(max_length=5, null=True, blank=True)
    cvc = models.CharField(max_length=3, null=True, blank=True)
    mpesa_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Payment {self.id} for {self.bus_name}"