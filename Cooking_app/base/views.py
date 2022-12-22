from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from .forms import SignupForm, LoginForm, PostForm, ProfileForm
from .models import *


@login_required(login_url='accounts/login')
def index(request):
    user = User.objects.get(username=request.user.username)
    context = {'user': user}

    return render(request, 'index.html')

@method_decorator(login_required(login_url='accounts/login'), name='dispatch')
class HomePageView(TemplateView):
    user = None
    context = {}
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
    
        user_info = UserInfo.objects.get(user=request.user)
        self.context = {
        
            'user_info': user_info
        }
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        pass
    


class Authentication(TemplateView):
    f_login = LoginForm
    f_signup = SignupForm
    context = {}
    template_name = 'login_signup.html'

    def get(self, request, *args, **kwargs):
        self.context = {
            'login_form': self.f_login(),
            'signup_form': list(self.f_signup(request=request)),
        }
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        # Case: Login information is submitted
        if 'login' in request.POST:
            form = self.f_login(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Email or Password is incorrect.")
            self.context = {
                'login_form': form,
                'signup_form': list(self.f_signup(request=request)),
            }
        # Case: Signup information is submitted
        if 'signup' in request.POST:
            form = self.f_signup(request.POST, request=request)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/')
            self.context = {
                'login_form': self.f_login(),
                'signup_form': list(form),
            }
        return render(request, self.template_name, self.context)

@method_decorator(login_required(login_url='accounts/login'), name='dispatch')
class Exit(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


@method_decorator(login_required(login_url='accounts/login'), name='dispatch')
class PersonalInfo(TemplateView):
    form_class = ProfileForm
    context = {}
    template_name = 'profile.html'

    def get(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            self.context = {
                'user_info': UserInfo.objects.get(user=user),
                'user': user,
                # 'user_recipes': UserRecipe.objects.filter(created_by=user_id),
            }
            print(self.context['user_info'].avatar.url)
            print('context is returned')
        except Exception as e:
            print(e)
            print("self.context")
            # messages.error(request, message=e)
        return render(request, self.template_name, self.context)

    def post(self, request, pk, *args, **kwargs):
        pass
    
    
@method_decorator(login_required(login_url='accounts/login'), name='dispatch')
class PostARecipeView(TemplateView):
    form = None
    context = {}
    template_name = 'post_a_recipe.html'
    
    def get(self, request, pk, *args, **kwargs):
        self.form = PostForm()        
        user = User.objects.get(id = pk)
        self.context = {
            'form': self.form,
            'user_info': UserInfo.objects.get(user=user),
        }
        return render(request, self.template_name, self.context)
    
    def post(self, request, pk, *args, **kwargs):
        
        user = User.objects.get(id = pk)
        self.context = {
            'user_info': UserInfo.objects.get(user=user),
        }
        form = self.form(request.POST)
        for name in request.POST.keys():
            print(f"\"{name}\":")
        return render(request, self.template_name, self.context)