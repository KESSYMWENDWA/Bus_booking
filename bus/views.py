from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Booking
from .models import Booking, Bus, Payment
from django.contrib import messages
from django.urls import reverse
from .models import Payment
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

@login_required
def buses_list(request):
    buses = Bus.objects.all()
    for bus in buses:
        bus.available_seats = range(1, bus.no_of_passengers + 1)
    return render(request, 'buses_list.html', {'buses': buses})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already taken'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered'

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # Create user and return success message
        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'status': 'success'})  # Success response

    return JsonResponse({'status': 'error', 'errors': {'form': 'Invalid request'}}, status=400)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': {'form': 'Invalid username or password'}}, status=400)
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def book_seat(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        from_location = request.POST.get('from')
        to_location = request.POST.get('to')
        date = request.POST.get('date')  # Date needs to be captured
        seat_number = int(request.POST.get('seat'))

        # Check if the seat is already booked for the same bus and same date
        if Booking.objects.filter(bus_id=bus_id, date=date, seat_number=seat_number).exists():
            # If seat is booked for the same date, return error response
            return JsonResponse({
                'status': 'error',
                'message': 'This seat is already booked for the selected date. Please choose a different seat.'
            }, status=400)

        # Otherwise, create the booking
        booking = Booking.objects.create(
            bus_id=bus_id,
            from_location=from_location,
            to_location=to_location,
            date=date,
            seat_number=seat_number,
            user=request.user  # Assuming the user is logged in
        )

        # Redirect to the payment page after successful booking
        payment_url = reverse('payment', args=[booking.id])
        
        # Return JSON response with the payment redirect URL
        return JsonResponse({
            'status': 'success',
            'message': 'Your seat has been successfully booked.',
            'redirect_url': payment_url
        })

    else:
        bus_id = request.GET.get('bus_id')
        bus = Bus.objects.get(id=bus_id)
        date = request.GET.get('date')
        
        # Get booked seats for this bus and date
        booked_seats = Booking.objects.filter(bus=bus, date=date).values_list('seat_number', flat=True)
        
        # Calculate available seats
        available_seats = [i for i in range(1, bus.no_of_passengers + 1) if i not in booked_seats]
        
        return render(request, 'book_seat.html', {
            'bus': bus,
            'available_seats': available_seats,
            'date': date  # Pass date to the template if needed
        })
@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    bus = booking.bus

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'card':
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvc = request.POST.get('cvc')
            mpesa_message = None
        else:  # M-Pesa
            card_number = None
            expiry_date = None
            cvc = None
            mpesa_message = request.POST.get('mpesa_message')

        # Create and save the payment record, assigning the logged-in user
        Payment.objects.create(
            user=request.user,  # Assign logged-in user
            booking=booking,
            bus_name=bus.name,
            route=bus.route,
            price=bus.price,
            seat_number=booking.seat_number,
            payment_method=payment_method,
            card_number=card_number,
            expiry_date=expiry_date,
            cvc=cvc,
            mpesa_message=mpesa_message
        )

        messages.success(request, "Payment processed successfully!")
        return redirect('bookings')  # Redirect to bookings page after successful payment

    return render(request, 'payment.html', {'bus': bus, 'booking': booking})

def bookings(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'payments': payments})