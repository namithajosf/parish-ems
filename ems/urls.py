from django.urls import path
from .views import index, app_calendar, user_account, view_account_details, app_kanban, add_parish_details, view_parish_details, add_event_type, add_role_details, view_role_details

urlpatterns = [
    path('', index, name='index'),
    path('app-calendar/', app_calendar, name='app_calendar'),
    path('app-kanban/', app_kanban, name='app_kanban'),
    path('parish-details/', add_parish_details, name='add_parish_details'),
    path("view-parish-details/", view_parish_details, name="view_parish_details"),
    path('add-event-type/', add_event_type, name='add_event_type'),
    path('account/', user_account, name='user_account'),
    path("view-account-details/", view_account_details, name="view_account_details"),
    path("add-role-details/", add_role_details, name="add_role_details"),
    path("view-role-details/", view_role_details, name="view_role_details"),



]