from django.contrib.auth import views as auth_views


from django.urls import reverse_lazy
from django.urls import path


from .forms import MySetPasswordForm, MyPasswordResetForm
from . import views


urlpatterns = [
    path('', views.home, name = 'index'),
    path('index/', views.home, name = 'index'),
    path('accounts/login/', views.login_acc, name = 'login'),
    path('accounts/signup/', views.signup_acc, name = 'signup'),
    path('accounts/logout/', views.logout_acc, name = 'logout'),
    path('accounts/profile/<str:pk>/', views.profile_acc, name = 'profile'),
    # path('accounts/password_reset/', views.rspw_acc, name = 'password_reset'),
    # path('accounts/password_reset/confirm/', views.rspw_acc_cf, name = 'password_reset_confirm'),
    # path('accounts/reset/<uidb64>/<token>/', views.rspw_acc, name = 'password_reset'),
    # path('accounts/password_reset/done/', views.rspw_acc_done, name = 'password_reset_done'), 
    # path('accounts/profile/', views.profile_acc, name = 'profile'),
    path(
        'accounts/password_reset/', 
        auth_views.PasswordResetView.as_view(
            form_class=MyPasswordResetForm,
            template_name='forgot_password.html',
            subject_template_name='password_reset_subject',
            email_template_name='password_reset_email.html',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'accounts/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='forgot_password1.html',
        ), 
        name='password_reset_done',
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            form_class=MySetPasswordForm,
            template_name='forgot_password2.html',
            success_url=reverse_lazy('login'),
        ),
        name='password_reset_confirm',
    ),
    path('post_a_recipe/', views.PostARecipe, name = 'post_a_recipe'),
]