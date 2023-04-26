from django import forms
from django.contrib.auth.models import User

from .models import Consultant, ConsultancyType, Feedback


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
                }),
            'password': forms.PasswordInput(attrs={
                'class': "form-control",
                }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'First Name'
                }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Last Name'
                }),
            
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]

class DateInput(forms.DateInput):
    input_type = 'date'


class ConsultantForm(forms.ModelForm):
    class Meta:
        model = Consultant
        exclude = ['user', 'ratings', 'number_of_reviews', 'number_of_customers', 'approved','first_name','last_name']
        widgets = {
            'phone_no': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Phone Number'
                }),
            'country': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Country'
                }),
            'address': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Address'
                }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'years of experience'
                }), 
        }

    def __init__(self, *args, **kwargs):
        super(ConsultantForm, self).__init__(*args, **kwargs)
        obj = ConsultancyType.objects.all()
        consultancy_types = []
        expertise = []
        for i in obj:
            consultancy_types.append((i.profession, i.profession))
            expertise.append((i.expertise, i.expertise))
        self.fields["type_of_consultant"].widget = forms.Select(choices=consultancy_types,attrs={
                'class': "form-control",
                })
        self.fields["expertise"].widget = forms.Select(choices=expertise,attrs={
                'class': "form-control",
                })



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('subject', 'description', 'ratings')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }