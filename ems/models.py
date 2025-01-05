from django.db import models

class Parish(models.Model):
    parish_name = models.CharField(max_length=255)
    parent_parish = models.CharField(max_length=255, null=True, blank=True)
    secretary_name = models.CharField(max_length=255, null=True, blank=True)
    place_of_parish = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    def __str__(self):
        return self.parish_name

class EventType(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    def __str__(self):
        return self.name
    
class UserRegistration(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    ROLE_CHOICES = [
        ('Public', 'Public'),
        ('Priest', 'Priest'),
        ('Secretary', 'Secretary'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Public')
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    parish = models.CharField(max_length=50)

    def __str__(self):
        return self.username

