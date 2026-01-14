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
from django.urls import path,include
from .views import *


app_name='resources'
urlpatterns = [
    path('<int:module_id>/', ResourceListView.as_view(), name='results'),
    path('resource/<int:resource_id>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('like/<int:resource_id>/', ToggleLikeView.as_view(), name='toggle_like'),
    path('save/<int:resource_id>/', ToggleSaveView.as_view(), name='toggle_save'),
    path('comment/<int:resource_id>/', AddCommentView.as_view(), name='add_comment'),
    path(
        'add/<int:module_id>/',
        AddResourceView.as_view(),
        name='add_resource'
    ),

]


