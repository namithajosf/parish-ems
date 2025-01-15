from django.urls import path
from .views import (
    index, app_calendar, app_kanban, 
    add_user_details, list_users, view_user_details, edit_user_details,   
    add_parish_details, list_parishes, view_parish_details, edit_parish_details,   
    add_role_details, list_roles, view_role_details, edit_role_details,     
    add_event_type, view_event_details
)

urlpatterns = [
    path('', index, name='index'),
    path('app-calendar/', app_calendar, name='app_calendar'),
    path('app-kanban/', app_kanban, name='app_kanban'),

    path('add-parish-details/', add_parish_details, name='add_parish_details'),
    path('list-parishes/', list_parishes, name='list_parishes'),
    path("view-parish-details/<int:parish_id>/", view_parish_details, name="view_parish_details"),
    path('edit-parish-details/<int:pk>/', edit_parish_details, name='edit_parish_details'),

    
    path('add-event-type/', add_event_type, name='add_event_type'),

    path('add-user-details/', add_user_details, name='add_user_details'),
    path('list-users/', list_users, name='list_users'),
    path("view-user-details/<int:user_id>/", view_user_details, name="view_user_details"),
    path('edit-user-details/<int:pk>/', edit_user_details, name='edit_user_details'),

    path('add-role-details/', add_role_details, name='add_role_details'),
    path('list-roles/', list_roles, name='list_roles'),
    path("view-role-details/<int:role_id>/", view_role_details, name="view_role_details"),
    path('edit-role-details/<int:pk>/', edit_role_details, name='edit_role_details'),

    path('view-event-details/', view_event_details, name='view_event_details'),
]
