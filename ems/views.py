from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
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
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect('app_calendar')
        else:
            messages.error(request, "There was an error adding the event. Please try again.")
    else:
        form = EventForm()

    event_types = EventType.objects.all()
    parishes = Parish.objects.all()
    return render(request, 'add-event-details.html', {
        'form': form,
        'event_types': event_types,
        'parishes': parishes,
    
    })

#<-----------------------------------------------------Assign Priest----------------------------------------------------------------->


def assign_priest(request, pk):
    # Get the event or return 404 if not found
    event = get_object_or_404(Event, id=pk)
    
    # Fetch all users with the 'Priest' role
    priests = UserRegistration.objects.filter(role__role='Priest')

    if request.method == 'POST':
        selected_priest_id = request.POST.get('priest')
        
        # Validate if the priest ID is valid and numeric
        if not selected_priest_id or not selected_priest_id.isdigit():
            messages.error(request, "Invalid priest selection. Please try again.")
            return render(request, 'assign-priest.html', {
                'event': event,
                'priests': priests,
            })
        
        # Fetch the selected priest or return 404 if it doesn't exist
        selected_priest = get_object_or_404(UserRegistration, id=int(selected_priest_id), role__role='Priest')
        
        # Assign the priest to the event
        event.priest = selected_priest
        event.save()

        # Get the parish email (recipient)
        parish_email = event.parish.email

        # Get the priest's email
        priest_email = selected_priest.email

        sender_email = 'aleenabenykk24@gmail.com'
        # Prepare the email subject and message for the parish
        subject_parish = f"Priest Assigned to Event: {event.event_name}"
        message_parish = f"The priest {selected_priest.username} has been successfully assigned to the event {event.event_name}."

        # Prepare the email subject and message for the priest (with event details)
        subject_priest = f"You have been assigned to the event: {event.event_name}"
        message_priest = f"""
        Dear {selected_priest.username},

        You have been successfully assigned to the event {event.event_name}.

        Event Details:
        - Event Name: {event.event_name}
        - Date: {event.event_date}
        - Time: {event.event_time}
        - Parish: {event.parish}
        - Description: {event.event_description if event.event_description else 'No description provided.'}

        Please mark this in your schedule and let us know if you need any further details.

        Best regards,
        Your Church Management System
        """

        # Send email to the parish and priest
        try:
            if parish_email:
                send_mail(subject_parish, message_parish, sender_email, [parish_email])

            if priest_email:
                send_mail(subject_priest, message_priest, sender_email, [priest_email])

            messages.success(request, f"Priest '{selected_priest.username}' assigned successfully. Emails sent to the parish and the priest.")
        except Exception as e:
            messages.error(request, f"Priest assigned, but there was an error sending the email: {str(e)}")

        # Redirect to list_events after assigning priest and sending emails
        return redirect('list_events')  # You can also keep it the same page or another page if you prefer

    # Render the form with event and available priests
    return render(request, 'assign-priest.html', {
        'event': event,
        'priests': priests,
    })

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
    events = Event.objects.all()
    return render(request, 'list-events.html', {'events': events})

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

def view_event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'view-event-details.html', {'event': event})

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




def edit_event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()  
            messages.success(request, "Event details updated successfully.")
            return redirect('edit_event_details', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'edit-event-details.html', {'form': form, 'event': event})


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
