from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Parish, Role, UserRegistration, EventType, Event
from .forms import RoleForm, ParishForm, UserRegistrationForm, EventTypeForm, EventForm

def index(request):
    return render(request, 'index.html')

def app_calendar(request):
    return render(request, 'app-calendar.html')

def settings(request):
    return render(request, 'settings.html')

# Role Management
def add_role_details(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role details saved successfully.")
            return redirect('add_role_details')
    else:
        form = RoleForm()
    return render(request, 'add-role-details.html', {'form': form})

def list_roles(request):
    roles = Role.objects.all()
    return render(request, "list-roles.html", {"roles": roles})

def view_role_details(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    return render(request, 'view-role-details.html', {'role': role})

def edit_role_details(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Role details updated successfully.")
            return redirect('edit_role_details', pk=role.pk)
        
    else:
        form = RoleForm(instance=role)

    return render(request, 'edit-role-details.html', {'form': form, 'role': role})

# Parish Management
def add_parish_details(request):
    if request.method == 'POST':
        form = ParishForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parish details saved successfully.")
            return redirect('add_parish_details')
    else:
        form = ParishForm()
    return render(request, 'add-parish-details.html', {'form': form})

def list_parishes(request):
    parishes = Parish.objects.all()
    return render(request, "list-parishes.html", {"parishes": parishes})

def view_parish_details(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    return render(request, 'view-parish-details.html', {'parish': parish})

def edit_parish_details(request, pk):
    parish = get_object_or_404(Parish, pk=pk)

    if request.method == 'POST':
        form = ParishForm(request.POST, instance=parish)
        if form.is_valid():
            form.save()
            messages.success(request, "Parish details updated successfully.")
            return redirect('edit_parish_details', pk=parish.pk)
        
    else:
        form = ParishForm(instance=parish)

    return render(request, 'edit-parish-details.html', {'form': form, 'parish': parish})

# User Account Management
def add_user_details(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            else:
                user = form.save(commit=False)
                user.password = make_password(password)
                user.save()
                messages.success(request, "Account saved successfully!")
                return redirect('add_user_details')
    else:
        form = UserRegistrationForm()

    parishes = Parish.objects.all()
    roles = Role.objects.all()

    return render(
        request, 
        'add-user-details.html', 
        {'form': form, 'parishes': parishes, 'roles': roles}
    )

def list_users(request):
    users = UserRegistration.objects.all()
    return render(request, "list-users.html", {"users": users})

def view_user_details(request, user_id):
    user = get_object_or_404(UserRegistration, id=user_id)
    return render(request, 'view-user-details.html', {'user': user})

def edit_user_details(request, pk):
    user = get_object_or_404(UserRegistration, pk=pk)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully.")
            return redirect('edit_user_details', pk=user.pk)
        
    else:
        form = UserRegistrationForm(instance=user)

    return render(request, 'edit-user-details.html', {'form': form, 'user': user})

# Event Management
def add_event_details(request):
    return render(request, 'add-event-details.html')

def list_events(request):
    return render(request, 'list-events.html')

def view_event_details(request):
    return render(request, 'view-event-details.html')

def edit_event_details(request):
    return render(request, 'edit-event-details.html')

def add_event_type_details(request):
    return render(request, 'add-event-type-details.html')

def list_event_types(request):
    return render(request, 'list-event-types.html')

def view_event_type_details(request):
    return render(request, 'view-event-type-details.html')

def edit_event_type_details(request):
    return render(request, 'edit-event-type-details.html')