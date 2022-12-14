from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
# Create your views here.

@login_required(login_url='accounts/login')
def home(request):
    return render(request, 'home.html')

def login_acc(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Email or Password is incorrect.")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login_signup.html', {'form': form})

def signup_acc(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            form = RegisterForm()
    return render(request, 'login_signup.html')