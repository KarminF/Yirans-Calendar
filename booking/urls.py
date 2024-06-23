from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    path('api/addbooking/', views.add_booking, name='add_booking'),
    path('api/delete/<booking_id>', views.delete_booking, name='delete_booking'),
]
