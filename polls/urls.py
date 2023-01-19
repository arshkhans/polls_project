from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name="loginUser"),
    path('logout/', views.logoutUser, name="logoutUser"),
    path('home/', views.home, name="home"),
    path('createPoll/', views.createPoll, name="createPoll"),
    path('profile/', views.viewProfile, name="viewProfile"),
    path('vote/', views.updateVote, name="updateVote"),
    path('checkVoted/', views.checkVoted, name="checkVoted"),
]