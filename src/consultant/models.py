from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField


# Create your models here.

def phone_validator(value):
    if len(str(value)) == 10:
        pass
    else:
        raise ValidationError('Phone Number sholud be of 10 digits')
    if value.isdigit():
        pass
    else:
        raise ValidationError('Phone Number sholud numbers only')


class Consultant(models.Model):
    """Model for Consultant"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10, validators=[phone_validator], default=9999999999)
    country = models.CharField(max_length=150)
    ratings = models.FloatField()
    number_of_reviews = models.IntegerField()
    number_of_customers = models.IntegerField()
    years_of_experience = models.IntegerField()
    type_of_consultant = models.CharField(max_length=150)
    expertise = models.CharField(max_length=150,default="")
    date_of_birth = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)

    class Meta:
        db_table = 'consultant_details'
    def __str__(self):
        return self.user.first_name
        

class ConsultancyType(models.Model):
    profession = models.CharField(max_length=150)
    expertise = models.CharField(max_length=250, default="")
    description = models.CharField(max_length=250)

    class Meta:
        db_table = 'consultancy_type'


class Portfolio(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    portfolio_name = models.CharField(max_length=150, unique=True)
    portfolio_description = models.CharField(max_length=150)

    class Meta:
        db_table = 'consultant_portfolio'



class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ratings = models.IntegerField(default=0)

    def __str__(self):
        return self.subject