from datetime import timedelta
from django import forms
from .models import Role, Parish, EventType, UserRegistration, Event
from .choices import STATUS_CHOICES, EVENT_STATUS_CHOICES

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role', 'status']
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES),
        }

class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = [
            'parish_name', 'parent_parish', 'secretary_name', 'place_of_parish',
            'address', 'email', 'contact_number', 'status'
        ]
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password",
    )
    parish = forms.ModelChoiceField(
        queryset=Parish.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Parish",
        empty_label="Select Parish",
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Role",
        empty_label="Select Role",
    )
    status = forms.ChoiceField(
        choices=[('Active', 'Active'), ('Inactive', 'Inactive')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status",
    )

    class Meta:
        model = UserRegistration
        fields = ['username', 'email', 'password', 'parish', 'role', 'status']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data

class EventForm(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    event_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_date', 'event_time', 'parish', 'priest', 'status', 'remarks', 'event_description']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'parish': forms.Select(attrs={'class': 'form-select'}),
            'priest': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].queryset = EventType.objects.all()
        self.fields['parish'].queryset = Parish.objects.all()
        self.fields['priest'].queryset = UserRegistration.objects.filter(role__role='Priest')



class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['event_type', 'duration', 'status']
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES),
        }

        def clean_duration(self):
            duration_str = self.cleaned_data['duration']
            hours, minutes = map(int, duration_str.split(':'))
            return timedelta(hours=hours, minutes=minutes)
