from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.home, name = 'index'),
    path('index/', views.home, name = 'index'),
    path('accounts/login/', views.login_acc, name = 'login'),
    path('accounts/signup/', views.signup_acc, name = 'signup'),
    path('accounts/profile/', views.profile_acc, name = 'profile'),
    path('accounts/logout/', views.logout_acc, name = 'logout'),
    path('post_a_recipe/', views.PostARecipe, name = 'post_a_recipe'),
    # path('accounts/logout', views.Exit.as_view(), name = 'logout'),
    # path('users/post/<str:pk>/', views.PersonalInfo.as_view(), name = 'profile'),
]