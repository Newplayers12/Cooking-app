from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'index'),
    path('index', views.HomePageView.as_view(), name = 'index'),
    path('post_a_recipe/<str:pk>/', views.PostARecipeView.as_view(), name = 'post_a_recipe'),
    path('accounts/login', views.Authentication.as_view(), name = 'login'),
    path('accounts/signup', views.Authentication.as_view(), name = 'signup'),
    path('accounts/logout', views.Exit.as_view(), name = 'logout'),
    path('users/profile/<str:pk>/', views.PersonalInfo.as_view(), name = 'profile'),
]