from django import forms
from .models import Role, Parish, EventType, UserRegistration, Event
from .choices import STATUS_CHOICES, EVENT_STATUS_CHOICES

# Form for Role model
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role', 'status']
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES),
        }

# Form for Parish model
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

# Form for EventType model
class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['name', 'duration']
        widgets = {
            'status': forms.Select(choices=EVENT_STATUS_CHOICES),
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
    class Meta:
        model = Event
        fields = [
            'event_name',
            'event_type',
            'event_date',
            'event_time',
            'event_description',
            'parish',
            'priest',
            'status',
            'remarks',
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'event_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'remarks': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
