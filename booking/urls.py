from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/bookings/', views.api_bookings, name='api_bookings'),
    path('book/', views.book_date, name='book'),
    # path('api/events/', views.get_events, name='get_events'),
    # path('api/add_event/', views.add_event, name='add_event'),
]