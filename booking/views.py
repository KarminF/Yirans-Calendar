import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import LoginFrom, RegistrationForm
from .models import Bookings


def index(request):
    return render(request, 'booking/index.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error('password', 'Incorrect username or password')
    else:
        form = LoginFrom()
    return render(request, 'booking/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save user to database and login automatically
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def api_bookings(request):
    # provide the list of events for the calendar to call
    booking_set = Bookings.objects.filter(user=request.user)
    bookings = []
    for booking in booking_set:
        booking_data = {
            'start': booking.start,
            'end': booking.end,
            'title': booking.title,
            'id': booking.booking_id,
        }
        bookings.append(booking_data)
    return JsonResponse(bookings, safe=False)


@login_required
def add_booking(request):
    # get booking info from ajax and add to database
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            Bookings.objects.create(start=data.get('start'), end=data.get('end'), title=data.get('title'), user=request.user, booking_id=data.get('booking_id'))
            return JsonResponse({'message': 'Booking successful!'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'invalid request'})


@login_required
def delete_booking(request, booking_id):
    # get booking id from ajax and delete booking from database
    if request.method == 'DELETE':
        try:
            Bookings.objects.filter(booking_id=booking_id).delete()
            return JsonResponse({'message': 'Booking deleted!'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    return JsonResponse({'message': 'invalid request'})
