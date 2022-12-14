from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('accounts/login', views.login_acc, name = 'login'),
    path('accounts/signup', views.signup_acc, name = 'signup'),

]