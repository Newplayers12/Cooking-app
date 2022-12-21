from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.index, name = 'index'),
    path('index', views.index, name = 'index'),
    path('accounts/login_signup', views.Authentication.as_view(), name = 'login_signup'),
]