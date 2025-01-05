from django.contrib import admin
from .models import Parish, Role, UserRegistration, EventType

# Register your models here.
admin.site.register(Parish)
admin.site.register(Role)
admin.site.register(UserRegistration)
admin.site.register(EventType)
