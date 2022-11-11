from django.contrib import admin
from django.urls import path
from apps import views 

urlpatterns = [
    # path('', views.index, name = "home"),
    path('', views.signIn),
    path('postsignIn/', views.loginPage),
    path('signUp/', views.signUp, name = "signup"),
    path('logout/', views.logout, name = "logout"),
    path('postsignUp/', views.postsignUp)
]
