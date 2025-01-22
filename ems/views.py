from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from .models import Parish, Role, UserRegistration, EventType, Event
from .forms import RoleForm, ParishForm, UserRegistrationForm, EventTypeForm, EventForm
from datetime import timedelta


def format_timedelta(duration):
    if isinstance(duration, timedelta):
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return str(duration)


def index(request):
    event_type = EventType.objects.first()
    event = Event.objects.first()
    parish = Parish.objects.first()
    role = Role.objects.first()
    user = UserRegistration.objects.first()

    context = {
        'event_type': event_type,
        'event': event,
        'parish': parish,
        'role': role,
        'user': user,
    }
    return render(request, 'index.html', context)

def app_calendar(request):
    return render(request, 'app-calendar.html')

def settings(request):
    return render(request, 'settings.html')

# <---------------------------------------------------------- Add details ---------------------------------------------------------->
def add_role_details(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role details saved successfully.")
            return redirect('list_roles')
    else:
        form = RoleForm()
    return render(request, 'add-role-details.html', {'form': form})

def add_parish_details(request):
    if request.method == 'POST':
        form = ParishForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parish details saved successfully.")
            return redirect('list_parishes')
    else:
        form = ParishForm()
    return render(request, 'add-parish-details.html', {'form': form})

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
                return redirect('list_users')
    else:
        form = UserRegistrationForm()

    parishes = Parish.objects.all()
    roles = Role.objects.all()

    return render(
        request, 
        'add-user-details.html', 
        {'form': form, 'parishes': parishes, 'roles': roles}
    )

def add_event_type_details(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Event Type details saved successfully.")
            return redirect('list_event_types')
    else:
        form = EventTypeForm()
    return render(request, 'add-event-type-details.html', {'form': form})

def add_event_details(request):
    return render(request, 'add-event-details.html')


# <---------------------------------------------------------- List details ---------------------------------------------------------->
def list_roles(request):
    search_query = request.GET.get('q', '')
    roles = Role.objects.filter(status="Active")

    if search_query:
        roles = roles.filter(
            Q(role__icontains=search_query)
        )

    paginator = Paginator(roles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "list-roles.html", {
        "page_obj": page_obj,
        "search_query": search_query,
    })

def list_parishes(request):
    search_query = request.GET.get('q', '')
    parishes = Parish.objects.filter(status="Active")

    if search_query:
        parishes = parishes.filter(
            Q(parish_name__icontains=search_query) | Q(secretary_name__icontains=search_query)
        )

    paginator = Paginator(parishes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list-parishes.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def list_users(request):
    search_query = request.GET.get('q', '')
    users = UserRegistration.objects.filter(status="Active")

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "list-users.html", {
        "page_obj": page_obj,
        "search_query": search_query,
    })

def list_event_types(request):
    
    search_query = request.GET.get('q', '')
    event_types = EventType.objects.filter(status="Active")

    if search_query:
        event_types = event_types.filter(
            Q(event_type__icontains=search_query)
        )

    paginator = Paginator(event_types, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "list-event-types.html", {
        "page_obj": page_obj,
        "search_query": search_query,
    })


def list_events(request):
    return render(request, 'list-events.html')


# <---------------------------------------------------------- View details ------------------------------------------------------------------>
def view_role_details(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    return render(request, 'view-role-details.html', {'role': role})

def view_parish_details(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    return render(request, 'view-parish-details.html', {'parish': parish})

def view_user_details(request, user_id):
    user = get_object_or_404(UserRegistration, id=user_id)
    return render(request, 'view-user-details.html', {'user': user})

def view_event_type_details(request, event_type_id):
    event_type = get_object_or_404(EventType, id=event_type_id)
    return render(request, 'view-event-type-details.html', {'event_type': event_type})

def view_event_details(request):
    return render(request, 'view-event-details.html')

# <---------------------------------------------------------- Edit details ---------------------------------------------------------->
def edit_role_details(request, pk):
    role = get_object_or_404(Role, pk=pk)

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Role details updated successfully.")
            return redirect('list_roles', pk=role.pk)
        
    else:
        form = RoleForm(instance=role)

    return render(request, 'edit-role-details.html', {'form': form, 'role': role})

def edit_parish_details(request, pk):
    parish = get_object_or_404(Parish, pk=pk)

    if request.method == 'POST':
        form = ParishForm(request.POST, instance=parish)
        if form.is_valid():
            form.save()
            messages.success(request, "Parish details updated successfully.")
            return redirect('list_parishes', pk=parish.pk)
        
    else:
        form = ParishForm(instance=parish)

    return render(request, 'edit-parish-details.html', {'form': form, 'parish': parish})

def edit_user_details(request, pk):
    user = get_object_or_404(UserRegistration, pk=pk)
    parishes = Parish.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully.")
            return redirect('list_users', pk=user.pk)
        
    else:
        form = UserRegistrationForm(instance=user)

    return render(
        request,
        'edit-user-details.html',
        {'form': form, 'parishes': parishes, 'roles': roles, 'user': user}
    )

def edit_event_type_details(request, pk):
    event_type = get_object_or_404(EventType, pk=pk)

    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=event_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Type details updated successfully.")

            return redirect('list_event_types', pk=event_type.pk)
        
    else:
        form = EventTypeForm(instance=event_type)
        event_type.duration_formatted = format_timedelta(event_type.duration)

    return render(request, 'edit-event-type-details.html', {'form': form, 'event_type': event_type})




def edit_event_details(request):
    return render(request, 'edit-event-details.html')


# <---------------------------------------------------------- Delete details ---------------------------------------------------------->
def delete_parish_details(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)

    parish.status = "Inactive"
    parish.save()

    return redirect('list_parishes')

def delete_role_details(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    role.status = "Inactive"
    role.save()

    return redirect('list_roles')

def delete_user_details(request, user_id):
    user = get_object_or_404(UserRegistration, id=user_id)

    user.status = "Inactive"
    user.save()

    return redirect('list_users')

def delete_event_type_details(request, event_type_id):
    event_type = get_object_or_404(EventType, id=event_type_id)

    event_type.status = "Inactive"
    event_type.save()

    return redirect('list_event_types')

# <---------------------------------------------------------- Trash ---------------------------------------------------------->

def show_trash(request):
    inactive_parishes = Parish.objects.filter(status='Inactive')
    inactive_roles = Role.objects.filter(status='Inactive')
    inactive_users = UserRegistration.objects.filter(status='Inactive')
    inactive_event_types = EventType.objects.filter(status='Inactive')
    

    context = {
        'inactive_parishes': inactive_parishes,
        'inactive_roles': inactive_roles,
        'inactive_users': inactive_users,
        'inactive_event_types': inactive_event_types,
    }
    return render(request, 'trash.html', context)

def restore_object(request, model_name, object_id):
    model = apps.get_model('ems', model_name) 
    
    obj = get_object_or_404(model, id=object_id)
    
    if hasattr(obj, 'status'):
        obj.status = 'Active'
        obj.save()
    
    messages.success(request, f"{model_name} restored successfully.")
    return redirect('trash')
