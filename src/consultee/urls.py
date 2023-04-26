from django.urls import path

from . import views

urlpatterns = [
    # path('', views.demo),
    path('register-consultee/', views.register_consultee, name='register_consultee'),
    path('view-consultant/<int:pk>/', views.view_consultant, name='view_consultant'),
    path('consultee-user-info', views.user_info, name='consultee_user_info'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    # path('appointment/', views.appointment_booking, name='appointment_booking'),
]
