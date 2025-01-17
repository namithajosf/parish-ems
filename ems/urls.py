from django.urls import path
from .views import (
    index, app_calendar, settings,
    add_user_details, list_users, view_user_details, edit_user_details,   
    add_parish_details, list_parishes, view_parish_details, edit_parish_details, delete_parish_details,  
    add_role_details, list_roles, view_role_details, edit_role_details, 
    add_event_details, list_events, view_event_details, edit_event_details,
    add_event_type_details, list_event_types, view_event_type_details, edit_event_type_details
)

urlpatterns = [
    path('', index, name='index'),
    path('app-calendar/', app_calendar, name='app_calendar'),
    path('settings/', settings, name='settings'),

    path('add-parish-details/', add_parish_details, name='add_parish_details'),
    path('list-parishes/', list_parishes, name='list_parishes'),
    path("view-parish-details/<int:parish_id>/", view_parish_details, name="view_parish_details"),
    path('edit-parish-details/<int:pk>/', edit_parish_details, name='edit_parish_details'),
    path('delete-parish-details/<int:parish_id>/', delete_parish_details, name='delete_parish_details'),

    path('add-user-details/', add_user_details, name='add_user_details'),
    path('list-users/', list_users, name='list_users'),
    path("view-user-details/<int:user_id>/", view_user_details, name="view_user_details"),
    path('edit-user-details/<int:pk>/', edit_user_details, name='edit_user_details'),

    path('add-role-details/', add_role_details, name='add_role_details'),
    path('list-roles/', list_roles, name='list_roles'),
    path("view-role-details/<int:role_id>/", view_role_details, name="view_role_details"),
    path('edit-role-details/<int:pk>/', edit_role_details, name='edit_role_details'),

    path('add-event-details/', add_event_details, name='add_event_details'),
    path('list-events/', list_events, name='list_events'),
    path("view-event-details/<int:event_id>/", view_event_details, name="view_event_details"),
    path('edit-event-details/<int:pk>/', edit_event_details, name='edit_event_details'),

    path('add-event-type-details/', add_event_type_details, name='add_event_type_details'),
    path('list-event-types/', list_event_types, name='list_event_types'),
    path("view-event-type-details/<int:event_id>/", view_event_type_details, name="view_event_type_details"),
    path('edit-event-type-details/<int:pk>/', edit_event_type_details, name='edit_event_type_details'),


]
