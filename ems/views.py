from django.shortcuts import render, redirect, get_object_or_404
from .models import Parish, UserRegistration, Role, EventType
from .forms import EventTypeForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

def app_calendar(request):
    return render(request, 'app-calendar.html')

def app_kanban(request):
    return render(request, 'app-kanban.html')

def add_role_details(request):
    if request.method == 'POST':
        role=request.POST.get('role')
        status = request.POST.get('status')

        Role.objects.create(
            role=role,
            status=status,
            created_time = timezone.now()
        )
    
        messages.success(request, "Role saved successfully.")
    return render(request, 'add-role-details.html')

def view_role_details(request):
    roles = Role.objects.all()
    return render(request, "view-role-details.html", {"roles": roles})


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

def view_parish_details(request):
    parishes = Parish.objects.all()
    return render(request, "view-parish-details.html", {"parishes": parishes})

def user_account(request):
    roles = Role.objects.all()
    parishes = Parish.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        parish_id = request.POST.get('parish')
        role_id = request.POST.get('role')
        status = request.POST.get('status')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('user_account')

        try:
            parish = Parish.objects.get(id=parish_id)
            role = Role.objects.get(id=role_id)

            UserRegistration.objects.create(
                username=username,
                password=make_password(password),
                email=email,
                contact_number=contact_number,
                parish=parish.parish_name,
                role=role.role,
                status=status
            )

            messages.success(request, "Account saved successfully!")
            return redirect('user_account')
        
        except Parish.DoesNotExist:
            messages.error(request, "Parish not found!")
        except Role.DoesNotExist:
            messages.error(request, "Role not found!")
        except Exception as e:
            messages.error(request, f"Failed to save user account: {str(e)}")
            print(f"Error saving user account: {str(e)}")
            return redirect('user_account')

    return render(request, 'account-details-form.html', {'roles': roles, 'parishes': parishes})

def view_account_details(request):
    users = UserRegistration.objects.all()
    return render(request, "view-account-details.html", {"users": users})


def add_event_type(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventTypeForm()
    return render(request, 'event-type-form.html', {'form': form})