from django import forms
from django.contrib.auth.models import User

from .models import Consultee
from administration.models import Appointment


class DateInput(forms.DateInput):
    input_type = 'date'


class Booking(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class ConsulteeForm(forms.ModelForm):
    class Meta:
        model = Consultee
        exclude = ['user']
        widgets = {
            'phone_no': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Phone Number'
                }),
            'country': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Country'
                }),
            'date_of_birth': DateInput(attrs={
                'class': "form-control",
                'placeholder': 'Phone Number'
                }),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]