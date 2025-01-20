from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from .models import Parish, Role, UserRegistration, EventType, Event
from .forms import RoleForm, ParishForm, UserRegistrationForm, EventTypeForm, EventForm

def index(request):
    return render(request, 'index.html')

def app_calendar(request):
    return render(request, 'app-calendar.html')

def settings(request):
    return render(request, 'settings.html')

# <---------- Add details --------->
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

def add_event_details(request):
    return render(request, 'add-event-details.html')

def add_event_type_details(request):
    return render(request, 'add-event-type-details.html')

# <--------- List details --------->
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
    return render(request, 'list-event-types.html')

def list_events(request):
    return render(request, 'list-events.html')


# <---------- View details --------->
def view_role_details(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    return render(request, 'view-role-details.html', {'role': role})

def view_parish_details(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    return render(request, 'view-parish-details.html', {'parish': parish})

def view_user_details(request, user_id):
    user = get_object_or_404(UserRegistration, id=user_id)
    return render(request, 'view-user-details.html', {'user': user})

def view_event_type_details(request):
    return render(request, 'view-event-type-details.html')

def view_event_details(request):
    return render(request, 'view-event-details.html')

# <--------- Edit details --------->
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

def edit_user_details(request, pk):
    user = get_object_or_404(UserRegistration, pk=pk)
    parishes = Parish.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User details updated successfully.")
            return redirect('edit_user_details', pk=user.pk)
        
    else:
        form = UserRegistrationForm(instance=user)

    return render(
        request,
        'edit-user-details.html',
        {'form': form, 'parishes': parishes, 'roles': roles, 'user': user}
    )

def edit_event_type_details(request):
    return render(request, 'edit-event-type-details.html')

def edit_event_details(request):
    return render(request, 'edit-event-details.html')


# <-------- Delete details ---------->
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

# <-------- Trash ---------->

def show_trash(request):
    inactive_parishes = Parish.objects.filter(status='Inactive')
    inactive_roles = Role.objects.filter(status='Inactive')
    inactive_users = UserRegistration.objects.filter(status='Inactive')

    context = {
        'inactive_parishes': inactive_parishes,
        'inactive_roles': inactive_roles,
        'inactive_users': inactive_users,
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
