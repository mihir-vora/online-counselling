from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='consultant_index'),
    path('register-consultant', views.register_consultant, name='register_consultant'),
    path('manage-appointment', views.manage_appointment, name='manage_appointment'),
    path('add-portfolio', views.add_portfolio, name='add_portfolio'),
    path('view-portfolio', views.view_portfolio, name='view_portfolio'),
    path('edit-portfolio/<int:pk>', views.edit_portfolio, name='edit_portfolio'),
    path('delete-portfolio/<int:pk>', views.delete_portfolio, name="delete_portfolio"),
    path('xyz', views.xyz, name='xyz'),
    path('user-info', views.user_info, name='user_info'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('post-feedback/', views.feedback, name='post-feedback'),

]
