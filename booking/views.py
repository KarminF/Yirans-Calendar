import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
@login_required
def book_date(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start = data.get('start')
        end = data.get('end')
        title = data.get('title')
        booking_id = data.get('booking_id')

        try:
            Bookings.objects.create(start=start, end=end, title=title, user=request.user, booking_id=booking_id)
            return JsonResponse({'status': 'success', 'message': 'Booking successful!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'invalid request'})


@csrf_exempt
@login_required
def delete_booking(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_id = data.get('id')
        try:
            Bookings.objects.filter(booking_id=booking_id).delete()
            return JsonResponse({'status': 'success', 'message': 'Booking deleted!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'invalid request'})
