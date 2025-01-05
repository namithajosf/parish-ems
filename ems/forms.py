from django import forms
from .models import Parish, EventType, UserRegistration

class ParishDetailsForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = [
            'parish_name',
            'parent_parish',
            'secretary_name',
            'place_of_parish',
            'address',
            'email',
            'contact_number',
            'status'
        ]
        widgets = {
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')]),
        }

class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['name', 'duration', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Baptism'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(in hours)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserRegistration
        fields = ['username', 'password', 'email', 'contact_number', 'role', 'status', 'parish']

