from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.index, name = 'index'),
    path('index', views.index, name = 'index'),
    path('accounts/login', views.login_signup, name = 'login'),
    path('accounts/signup', views.login_signup, name = 'signup'),
]