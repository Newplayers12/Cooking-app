from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.home, name = 'index'),
    path('index/', views.home, name = 'index'),
    path('accounts/login/', views.login_acc, name = 'login'),
    path('accounts/signup/', views.signup_acc, name = 'signup'),
    path('accounts/logout/', views.logout_acc, name = 'logout'),
    path('accounts/profile/<str:pk>/', views.profile_acc, name = 'profile'),
    path('accounts/password_reset/', views.rspw_acc, name = 'password_reset'),
    # path('accounts/password_reset/confirm/', views.rspw_acc_cf, name = 'password_reset_confirm'),
    # path('accounts/reset/<uidb64>/<token>/', views.rspw_acc, name = 'password_reset'),
    # path('accounts/password_reset/done/', views.rspw_acc_done, name = 'password_reset_done'), 
    path('post_a_recipe/', views.PostARecipe, name = 'post_a_recipe'),
    # path('accounts/logout', views.Exit.as_view(), name = 'logout'),
    # path('users/post/<str:pk>/', views.PersonalInfo.as_view(), name = 'profile'),
]