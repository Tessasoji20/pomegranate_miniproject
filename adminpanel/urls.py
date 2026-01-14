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

from django.urls import path
from .views import *

app_name = 'admin_panel'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('posts/', AdminPostListView.as_view(), name='posts'),
    path('posts/<int:post_id>/', AdminPostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/delete/', AdminDeletePostView.as_view(), name='delete_post'),
    path('comments/<int:comment_id>/delete/', AdminDeleteCommentView.as_view(), name='delete_comment'),
    path('users/', AdminUsersView.as_view(), name='users'),
    # path('subjects/', AdminSubjectsView.as_view(), name='subjects'),
    path('flags/', AdminFlaggedView.as_view(), name='flags'),
    path('posts/<int:post_id>/flag/', AdminFlagPostView.as_view(), name='flag_post'),
    path('comments/<int:comment_id>/flag/', AdminFlagCommentView.as_view(), name='flag_comment'),


]
