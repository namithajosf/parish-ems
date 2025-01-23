from django.contrib import admin
from .models import Parish, Role, UserRegistration, EventType, Event

# Register your models here.
admin.site.register(Parish)
admin.site.register(Role)
admin.site.register(UserRegistration)
admin.site.register(EventType)
admin.site.register(Event)