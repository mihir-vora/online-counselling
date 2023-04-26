from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .forms import ConsulteeForm,Booking

from consultant.forms import UserForm, UserUpdateForm
from administration.models import UserRole,Appointment
from consultant.models import Consultant
from django.contrib.auth.decorators import login_required

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import joblib

# Create your views here.
def demo(request):
    return HttpResponse('In Consultee')

CONSULTEE = None

def register_consultee(request):
    CONSULTEE = 'consultee'
    if request.method == 'GET':
        user_form = UserForm()
        consultee_form = ConsulteeForm()
        context = {}
        context['user_form'] = user_form
        context['consultee_form'] = consultee_form
        return render(request, 'consultee/registeration-form.html', context)
    else:
        user_form = UserForm(request.POST)
        consultee_form = ConsulteeForm(request.POST)
        user_role = UserRole()
        context = {}
        context['user_form'] = user_form
        context['consultee_form'] = consultee_form
        if user_form.is_valid() and consultee_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user_role.user = user
            user_role.role = 'Consultee'
            user_role.save()
            consultee = consultee_form.save(commit=False)
            consultee.user = user
            consultee.ratings = 0
            consultee.number_of_reviews = 0
            consultee.number_of_customers = 0
            consultee.save()
            return redirect('login_user')
        else:
            return render(request, 'consultee/registeration-form.html', context)


def view_consultant(request, pk):
    if request.method == 'GET':
            
        consultant = Consultant.objects.get(id=pk,approved=True)
        print(consultant.country)
        
        return render(request, 'consultee/viewConsultant.html', {'consultant': consultant})
    else:
        consultant_new = Consultant.objects.get(id=pk)
        consultee_new = request.user
        date = request.POST.get('date')
        print('date',date)
        time = request.POST.get('time')
        print('time',time)
        datetime = date+' '+time
        booking_data = Booking(request.POST)
        print(booking_data)
        Appointment.objects.create(consultant=consultant_new,consultee = consultee_new,date_time_stamp = datetime,remark = request.POST.get('remark'))
        return render(request, 'consultee/bookingconfirm.html')


@login_required
def user_info(request):
    user = User.objects.get(username=request.user.username)

    username = user.username
    email = user.email
    password = user.password
    first_name = user.first_name
    last_name = user.last_name


    return render(request, 'consultee/consultee_user_info.html', {'username': username, 'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name, 'consultee' : CONSULTEE})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)

        if uform.is_valid():
            uform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('user_info')
    else:
        uform = UserUpdateForm(instance=request.user)

    return render(request, 'consultee/edit_profile.html', {'uform': uform,})
