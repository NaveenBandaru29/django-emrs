from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.Index,name="index"),
    path("home", views.Home,name="home"),
    path("about", views.About,name="about"),
    path("contact", views.ContactUs,name="contact"),
    path("login", views.Login,name="login"),
    path("logout", views.Logout,name="logout"),
    path("signup", views.SignUp,name="signup"),
    path("profile", views.profile,name="profile"),
    path("play", views.playSongs,name="play"),
    path("run", views.run,name="run"),
    path("onlyHappy", views.onlyHappy,name="onlyHappy"),
    path("onlyNeutral", views.onlyHappy,name="onlyNeutral"),
    path("onlySad", views.onlySad,name="onlySad"),

]