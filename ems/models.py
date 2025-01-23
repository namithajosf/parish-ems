from django.db import models
from .choices import STATUS_CHOICES, EVENT_STATUS_CHOICES


class Role(models.Model):
    role = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role


class Parish(models.Model):
    parish_name = models.CharField(max_length=255)
    parent_parish = models.CharField(max_length=255, null=True, blank=True)
    secretary_name = models.CharField(max_length=255, null=True, blank=True)
    place_of_parish = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True)
    contact_number = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.parish_name



class UserRegistration(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.parish}"


class EventType(models.Model):
    event_type = models.CharField(max_length=100)
    duration = models.DurationField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    def __str__(self):
        return self.event_type


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_description = models.TextField(null=True, blank=True)

    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    priest = models.ForeignKey(
        UserRegistration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role__role': 'Priest'}
    )
    status = models.CharField(max_length=15, choices=EVENT_STATUS_CHOICES, default='Scheduled')
    remarks = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name
