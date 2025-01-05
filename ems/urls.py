from django.urls import path
from .views import index, app_calendar, user_account, app_kanban, add_parish_details, add_event_type

urlpatterns = [
    path('', index, name='index'),
    path('app-calendar/', app_calendar, name='app_calendar'),
    path('app-kanban/', app_kanban, name='app_kanban'),
    path('parish-details/', add_parish_details, name='add_parish_details'),
    path('add-event-type/', add_event_type, name='add_event_type'),
    path('account/', user_account, name='user_account'),
]