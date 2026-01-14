"""
URL configuration for pomegranate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path


from app.views import (
    SplashView,
    LoginView,
    Register,
    HomeView,
    ChooseCourseView,
    ChooseSemesterView,
    ChooseSubjectView,
    ProfileView,
    LogoutView,
    ChooseModuleView,
)



app_name = 'app'
urlpatterns = [
    path('',SplashView.as_view(), name='splash'),
    path('login',LoginView.as_view(),name='userlogin'),
    path('logout', LogoutView.as_view(), name='userlogout'),

    path('register',Register.as_view(),name='register'),
    path('choose-course',ChooseCourseView.as_view(),name='choose_course'),
    path('choose-semester',ChooseSemesterView.as_view(),name='choose_semester'),

    path('dashboard',HomeView.as_view(),name='dashboard'),
    path('dashboard/userprofile',ProfileView.as_view(),name='profile'),
    path('dashboard/selectsubject',ChooseSubjectView.as_view(),name='select_subject'),
    path(
        'dashboard/modules/<int:subject_id>/',
        ChooseModuleView.as_view(),
        name='choose_module'
    ),
]
