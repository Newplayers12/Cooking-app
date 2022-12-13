from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='signin')
def index(requests):
    return render(requests, 'index.html')

@login_required(login_url='signin')
def settings(requests):
    return render(requests, 'setting.html')


def signup(requests):
    if requests.method == 'POST': 
        username = requests.POST['username']
        email = requests.POST['email']
        password = requests.POST['password']
        password_2 = requests.POST['confirm_password']
        # print(username, email, password, password_2)
        if (password == password_2):
            if User.objects.filter(email=email).exists():
                messages.info(requests, 'Email Taken') # maybe this we code change later on
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(requests, 'Username Taken') # maybe this we code change later on
                return redirect('signup')
            else: # Create new user
                user = User.objects.create_user(username=username, password=password, email = email)
                user.save()

                # log user in and redirect sign in page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(requests, user_login)
                
                # create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(requests, 'Password not matching')
            return redirect('signup')
        
    else:
        return render(requests, 'signup.html')


def signin(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']
        user = auth.authenticate(username=username, password=password) # if there is a user, return not None
        if user is not None:
            auth.login(requests, user)
            return redirect('/')
        else: # doesnt exists
            messages.info(requests, 'Credentials Invalid')
            return redirect('signin')
            
    return render(requests, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

