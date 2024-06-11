import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginFrom, RegistrationForm, EventForm
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

        try:

            if Bookings.objects.filter((Q(start__lte=start) & Q(end__gte=start)) | (Q(start__lte=end) & Q(end__gte=end))):
                return JsonResponse({'status': 'error', 'message': 'This time period is already booked.'})

            booking = Bookings.objects.create(start=start, end=end, title=title, user=request.user)
            return JsonResponse({'status': 'success', 'message': 'Booking successful!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'invalid request'})


def test(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            # 在这里你可以处理事件名称，比如保存到数据库中
            # 这里只是简单的打印出来
            print("Event Name:", event_name)
    else:
        form = EventForm()
    return render(request, 'booking/test.html', {'form': form})
