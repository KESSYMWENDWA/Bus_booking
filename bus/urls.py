from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage URL
    path('buses/', views.buses_list, name='buses'),  # List of buses
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('book/', views.book_seat, name='book_seat'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('bookings/', views.bookings, name='bookings'),

]
