from django.shortcuts import render, redirect
from .models import Parish, UserRegistration, Role
from .forms import EventTypeForm
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


def user_account(request):
    roles = Role.objects.all()
    parishes = Parish.objects.all()

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        parish_id = request.POST.get('parish')
        role_id = request.POST.get('role')
        status = request.POST.get('status')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('user_account')
        
        try:
            parish = Parish.objects.get(id=parish_id)
            role = Role.objects.get(id=role_id)

            user = UserRegistration(
                username=username,
                password=password,
                parish=parish,
                role=role,
                status=status
            )
            user.save()

            messages.success(request, "Account saved successfully!")
            return redirect('user_account')
        
        except Parish.DoesNotExist:
            messages.error(request, "Parish not found!")
        except Role.DoesNotExist:
            messages.error(request, "Role not found!")

    return render(request, 'account-details-form.html', {'roles': roles, 'parishes': parishes})

def add_event_type(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventTypeForm()
    return render(request, 'event-type-form.html', {'form': form})