from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.home, name ="home"),
    path('live/', views.livefe, name ="live"),
    path('details/', views.respond, name ="table"),
    path('add/', views.addStudents, name ="add"),
    path('', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]

