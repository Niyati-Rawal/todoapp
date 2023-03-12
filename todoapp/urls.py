from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',customloginview.as_view(),name='login'),
    path('register/',registeruser.as_view(),name='register'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/',taskdetail.as_view(),name='task'),
    path('task-create/',taskcreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',taskupdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',taskdelete.as_view(),name='task-delete'),

    
]