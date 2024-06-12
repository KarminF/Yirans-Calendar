from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    path('api/book/', views.book_date, name='book_date'),
    path('api/delete/', views.delete_booking, name='delete_booking'),
]
