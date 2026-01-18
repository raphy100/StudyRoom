from django.urls import path
from . import views 
from django.views.generic.base import RedirectView


urlpatterns = [
    path('login/', views.LoginPage, name ="login"),
    path('register/', views.registerUser, name ="register"),
    path('logout/', views.logoutUser, name ="logout"),
    path('', views.home, name ="home"),
    path('room/<str:pk>/', views.room, name ="room"),
    path('room/<str:pk>/participants/', views.participants, name='participants'),
    path('profile/<str:pk>/', views.userprofile, name ="user-profile"),
    path('create-room/', views.createRoom, name ="create-room"),
    path('create-room.html', RedirectView.as_view(pattern_name='create-room', permanent=True)),
    path('update-room/<str:pk>/', views.updateRoom, name ="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name ="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name ="delete-message"),
    path('update-user/', views.updateUser, name ="update-user"),
    path('topics/', views.topicsPage, name ="topics"),
    path('activity/', views.activityPage, name ="activity"),
]