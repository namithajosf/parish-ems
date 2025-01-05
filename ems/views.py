from django.shortcuts import render, redirect
from .models import Parish
from .forms import EventTypeForm, UserRegistrationForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def app_calendar(request):
    return render(request, 'app-calendar.html')

def app_kanban(request):
    return render(request, 'app_kanban.html')

def add_parish_details(request):
    if request.method == 'POST':
        parish_name = request.POST.get('parish_name')
        parent_parish = request.POST.get('parent_parish')
        secretary_name = request.POST.get('secretary_name')
        place_of_parish = request.POST.get('place_of_parish')
        address = request.POST.get('address')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        status = request.POST.get('status')

        Parish.objects.create(
            parish_name=parish_name,
            parent_parish=parent_parish,
            secretary_name=secretary_name,
            place_of_parish=place_of_parish,
            address=address,
            email=email,
            contact_number=contact_number,
            status=status,
        )

        messages.success(request, "Parish details saved successfully.")
        return redirect('add_parish_details')
    return render(request, 'parish-details-form.html')


def add_event_type(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventTypeForm()
    return render(request, 'event-type-form.html', {'form': form})

def user_account(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_account')
    else:
        form = UserRegistrationForm()
    return render(request, 'account-details-form.html', {'form': form})
