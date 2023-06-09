import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
import pandas as pd
from django.contrib.auth.models import User
from .forms import UserUpdateForm
from administration.models import UserRole
from consultant.models import ConsultancyType, Consultant, Feedback
from consultee.models import Consultee
from .models import Country, State, City


# Create your views here.
def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def admin_info(request):
    user = User.objects.get(username=request.user.username)

    username = user.username
    email = user.email
    password = user.password


    return render(request, 'administration/admin_info.html', {'username': username, 'email': email, 'password': password,})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)

        if uform.is_valid():
            uform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('admin_user_info')
    else:
        uform = UserUpdateForm(instance=request.user)

    return render(request, 'administration/edit_admin_profile.html', {'uform': uform,})




@login_required
def administration_index(request):
    context = {}
    total_consultant_objects = Consultant.objects.count()
    total_consultee_objects = Consultee.objects.count()
    total_feedback_objects = Feedback.objects.count()
    context['total_consultant_objects'] = total_consultant_objects
    context['total_consultee_objects'] = total_consultee_objects
    context['total_feedback_objects'] = total_feedback_objects
    if request.user.is_superuser:
        return render(request, 'administration/index.html', context)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'administration/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print(user)
                if request.user.is_superuser:
                    return redirect('administration_index')
                else:
                    user_role = UserRole.objects.get(user=user)
                    if user_role.role == 'Consultant':
                        return redirect('consultant_index')
                    elif user_role.role == 'Consultee':
                        return redirect('index')
            else:
                return HttpResponse('User Is Not Active.')
        else:
            # message = 'Login failed!'
            # return render(request,'administration/login.html', context={'messages': message})
            messages.error(request, 'Invalid Login Credentials')
            # print("sadasda",msg)
            # return render(request,'administration/login.html', {'messages':msg})
        return render(request, 'administration/login.html')


@login_required
def view_profile(request, id):
    return HttpResponse('Hello')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required
def approve_consultant(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            unapproved_consultants = Consultant.objects.all()
            print(unapproved_consultants)
            return render(request, 'administration/approveConsultant.html', {'unapproved_consultants': unapproved_consultants})


@login_required
def approve_consultant_action(request, pk):
    if request.user.is_superuser:
        consultant = Consultant.objects.get(id=pk)
        consultant.approved = True
        consultant.save()
        return redirect('approve_consultant')


@login_required
def view_consultee(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            consultee = Consultee.objects.all()
            return render(request, 'administration/viewConsultee.html', {'consultee': consultee})


@login_required
def view_consultancy_type(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            context = {}
            context['consultancy_type'] = ConsultancyType.objects.all()
            return render(request, 'administration/viewConsultancyType.html', context)


@login_required
def add_consultancy_type(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'administration/addConsultancyType.html')
        else:
            consultancy_type = ConsultancyType()
            consultancy_type.profession = request.POST['consultancy-type']
            consultancy_type.expertise = request.POST['consultancy-expertise']
            consultancy_type.description = request.POST['consultancy-description']
            consultancy_type.save()
            return redirect('view_consultancy_type')


@login_required
def add_country(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'administration/addCountry.html')
        else:
            # print(request.POST)
            country = Country()
            country.country_name = request.POST['country-name']
            country.country_description = request.POST['country-description']
            country.save()
            messages.success(request, 'Country Added Successfully')
            return redirect('view_country')


@login_required
def view_country(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            countries = Country.objects.all()
            context = {}
            context['countries'] = countries
            return render(request, 'administration/viewCountry.html', context)


@login_required
def add_state(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            countries = Country.objects.all()
            context = {}
            context['countries'] = countries
            return render(request, 'administration/addState.html', context)
        else:
            country = Country.objects.get(id=request.POST['country'])
            state = State()
            state.country = country
            state.state_name = request.POST['state-name']
            state.state_description = request.POST['state-description']
            state.save()
            return redirect('view_state')


@login_required
def view_state(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            states = State.objects.all()
            context = {}
            context['states'] = states
            return render(request, 'administration/viewState.html', context)


@login_required
def add_city(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            countries = Country.objects.all()
            context = {}
            context['countries'] = countries
            return render(request, 'administration/addCity.html', context)
        else:
            country = Country.objects.get(id=request.POST['country'])
            state = State.objects.get(id=request.POST['state'])
            city = City()
            city.country = country
            city.state = state
            city.city_name = request.POST['city-name']
            city.city_description = request.POST['city-description']
            city.save()
            return redirect('view_city')


@login_required
def view_city(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            cities = City.objects.all()
            context = {}
            context['cities'] = cities
            return render(request, 'administration/viewCity.html', context)


@login_required
def view_appointments(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'administration/viewAppointments.html')


@login_required
def view_complaints(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'administration/viewComplaints.html')


@login_required
def view_feedbacks(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            feedbacks_data = Feedback.objects.all()
            context = {}

            context['feedbacks_data'] = feedbacks_data
            return render(request, 'administration/viewFeedbacks.html', context)


@login_required
def delete_country(request, pk):
    if request.user.is_superuser:
        Country.objects.get(id=pk).delete()
        return redirect('view_country')


@login_required
def edit_country(request, pk):
    if request.user.is_superuser:
        country = Country.objects.get(id=pk)
        if request.method == 'GET':
            context = {}
            context['country'] = country
            return render(request, 'administration/editCountry.html', context)
        else:
            country.country_name = request.POST['country-name']
            country.country_description = request.POST['country-description']
            country.save()
            return redirect('view_country')


@login_required
def delete_state(request, pk):
    if request.user.is_superuser:
        State.objects.get(id=pk).delete()
        return redirect('view_state')


@login_required
def edit_state(request, pk):
    if request.user.is_superuser:
        countries = Country.objects.all()
        state = State.objects.get(id=pk)
        if request.method == 'GET':
            context = {}
            context['countries'] = countries
            context['state'] = state
            return render(request, 'administration/editState.html', context)
        else:
            state.country = Country.objects.get(id=request.POST['country'])
            state.state_name = request.POST['state-name']
            state.state_description = request.POST['state-description']
            state.save()
            return redirect('view_state')


@login_required
def get_states(request, pk):
    if request.user.is_superuser:
        country = Country.objects.get(id=pk)
        states = list(State.objects.filter(country=country).values())
        return HttpResponse(json.dumps(states))


@login_required
def delete_city(request, pk):
    if request.user.is_superuser:
        City.objects.get(id=pk).delete()
        return redirect('view_city')


@login_required
def edit_city(request, pk):
    if request.user.is_superuser:
        countries = Country.objects.all()
        states = State.objects.all()
        city = City.objects.get(id=pk)
        if request.method == 'GET':
            context = {}
            context['countries'] = countries
            context['states'] = states
            context['city'] = city
            return render(request, 'administration/editCity.html', context)
        else:
            city.country = Country.objects.get(id=request.POST['country'])
            city.state = State.objects.get(id=request.POST['state'])
            city.city_name = request.POST['city-name']
            city.city_description = request.POST['city-description']
            city.save()
            return redirect('view_city')


@login_required
def edit_consultancy_type(request, pk):
    if request.user.is_superuser:
        consultancy_type = ConsultancyType.objects.get(id=pk)
        if request.method == 'GET':
            context = {}
            context['consultancy_type'] = consultancy_type
            return render(request, 'administration/editConsultancyType.html', context)
        else:
            consultancy_type.profession = request.POST['consultancy-profession']
            consultancy_type.expertise = request.POST['consultancy-expertise']
            consultancy_type.description = request.POST['consultancy-description']
            consultancy_type.save()
            return redirect('view_consultancy_type')


@login_required
def delete_consultancy_type(request, pk):
    if request.user.is_superuser:
        consultancy_type = ConsultancyType.objects.get(id=pk).delete()
        return redirect('view_consultancy_type')


@login_required
def delete_consultee(request, pk): 
    if request.user.is_superuser:
        Consultee.objects.get(id=pk).delete()
        return redirect('view_consultee')


@login_required
def search_consultancy_type(request, c_type):
    consultants = Consultant.objects.filter(
        type_of_consultant=c_type.title(), approved=True)
    print(consultants)

    return render(request, 'administration/searchPage.html', {'consultants': consultants})


@login_required
def search_category(request):

    print(request.POST['types'])
    consultants = Consultant.objects.filter(
        expertise__icontains=request.POST['types'], approved=True)
    print(consultants)
    return render(request, 'administration/searchPage.html/', {'consultants': consultants})



def abc(request):
    products = list(Consultant.objects.all().values())
    df = pd.DataFrame(products)
    print(df)
    return HttpResponse('Hello World')
