from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.home_user, name = 'index'),
    path('index/', views.home_user, name = 'index'),
    path('accounts/login/', views.login_acc, name = 'login'),
    path('accounts/signup/', views.signup_acc, name = 'signup'),
    # path('asdasdasd adas/', views......, name="logout")
    # path('post_a_recipe/<str:pk>/', views.PostARecipeView.as_view(), name = 'post_a_recipe'),
    # path('accounts/logout', views.Exit.as_view(), name = 'logout'),
    # path('users/post/<str:pk>/', views.PersonalInfo.as_view(), name = 'profile'),
]