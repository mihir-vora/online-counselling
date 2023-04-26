from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from administration.models import UserRole
from .forms import UserForm, ConsultantForm, UserUpdateForm, FeedbackForm
from .models import Portfolio, Consultant
from administration.models import Appointment

import pandas as pd

# Create your views here.
@login_required
def index(request):
    response = render(request, 'consultant/index.html')
    response.set_cookie('role', 'consultant')
    return response


def register_consultant(request):
    if request.method == 'GET':
        user_form = UserForm()
        consultant_form = ConsultantForm()
        context = {}
        context['user_form'] = user_form
        context['consultant_form'] = consultant_form
        return render(request, 'consultant/registeration-form.html', context)
    else:
        user_form = UserForm(request.POST)
        consultant_form = ConsultantForm(request.POST)
        user_role = UserRole()
        context = {}
        context['user_form'] = user_form
        context['consultant_form'] = consultant_form
        if user_form.is_valid() and consultant_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user_role.user = user
            user_role.role = 'Consultant'
            user_role.save()
            consultant = consultant_form.save(commit=False)
            consultant.user = user
            consultant.ratings = 0
            consultant.number_of_reviews = 0
            consultant.number_of_customers = 0
            consultant.save()
            return redirect('login_user')
        else:
            return render(request, 'consultant/registeration-form.html', context)


@login_required
def manage_appointment(request):
    if request.COOKIES['role'] == 'consultant':
        booking_data = Appointment.objects.all()
        return render(request, 'consultant/manageAppointment.html',{'booking_data':booking_data})
    else:
        print('hello world')


@login_required
def add_portfolio(request):
    if request.COOKIES['role'] == 'consultant':
        if request.method == 'GET':
            return render(request, 'consultant/addPortfolio.html')
        else:
            portfolio = Portfolio()
            portfolio.portfolio_name = request.POST['portfolio-name']
            portfolio.portfolio_description = request.POST['portfolio-description']
            portfolio.consultant = Consultant.objects.get(user=User.objects.get(username=request.user.username))
            try:
                portfolio.save()
            except:
                messages.error(request, 'Portfolio Name should be unique!!')
                return redirect('add_portfolio')

            return redirect('view_portfolio')


@login_required
def view_portfolio(request):
    if request.COOKIES['role'] == 'consultant':
        if request.method == 'GET':
            context = {}
            portfolio = Portfolio.objects.all()
            context['portfolio'] = portfolio
            return render(request, 'consultant/viewPortfolio.html', context)


def xyz(request):
    data = pd.DataFrame(list(Consultant.objects.all().values()))
    print(data)
    data.to_csv('database_data.csv')
    return 'abc'

@login_required
def user_info(request):
    user = User.objects.get(username=request.user.username)

    username = user.username
    email = user.email
    password = user.password
    first_name = user.first_name
    last_name = user.last_name


    return render(request, 'consultant/user_info.html', {'username': username, 'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name})


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

    return render(request, 'consultant/edit_profile.html', {'uform': uform,})

@login_required
def edit_portfolio(request, pk):
    portfolio_type = Portfolio.objects.get(id=pk)
    if request.method == 'GET':
        context = {}
        context['portfolio_type'] = portfolio_type
        return render(request, 'consultant/edit_portfolio.html', context)
    else:
        portfolio_type.portfolio_name = request.POST['portfolio_name']
        portfolio_type.portfolio_description = request.POST['portfolio_description']
        portfolio_type.save()
        return redirect('view_portfolio')

@login_required
def delete_portfolio(request, pk):
    consultancy_type = Portfolio.objects.get(id=pk).delete()
    return redirect('view_portfolio')



@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted.')
            return redirect('post-feedback')
    else:
        form = FeedbackForm()

    context = {'form': form}
    return render(request, 'consultant/feedback.html', context)
