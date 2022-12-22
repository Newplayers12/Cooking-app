from django.views.generic import TemplateView
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password
# from .forms import SignupForm, LoginForm, ProfileForm
from .models import UserInfo, UserRecipe


@login_required(login_url='accounts/login')
def index(request):
    return render(request, 'index.html')


def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('input')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        context = {
            'username': username,
        }
        print(username)
        if user is None:
            messages.error(request, 'invalid username or password')
            return render(request, 'login_signup.html', context)
        login(request, user)
        return redirect('/') 
    
    return render(request, 'login_signup.html', context)

def signup_user(request):
    context = {}
    template_name = 'login_signup.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        gender = 'C'
        context = {
            'username': username,
            'fullname': fullname,
            'email': email,
            'gender': gender,
        }
        print(username, password1, password2, fullname, email, gender)
        
        
        if (password1 != password2):
            messages.error(request, 'passwords do not match')
            
            return render(request, template_name, context)

        user = User.objects._user(username=username, password=make_password(password1), email=email)
        
        user_info = UserInfo.objects.create(user=user, fullname=fullname, gender=gender[0])
        login(request, user)
        return redirect('/')
    
    return render(request, template_name, context)
    
        





        

        

# class Authentication(TemplateView):
#     f_login = LoginForm
#     f_signup = SignupForm
#     context = {}
#     template_name = 'login_signup.html'

#     def get(self, request, *args, **kwargs):
#         self.context = {
#             'login_form': self.f_login(),
#             'signup_form': list(self.f_signup(request=request)),
#         }
#         return render(request, self.template_name, self.context)
    
#     def post(self, request, *args, **kwargs):
#         # Case: Login information is submitted
#         if 'login' in request.POST:
#             form = self.f_login(request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')
#                 user = authenticate(request, username=username, password=password)
#                 if user:
#                     login(request, user)
#                     return redirect('/')
#                 else:
#                     messages.error(request, "Email or Password is incorrect.")
#             self.context = {
#                 'login_form': form,
#                 'signup_form': list(self.f_signup(request=request)),
#             }
#         # Case: Signup information is submitted
#         if 'signup' in request.POST:
#             form = self.f_signup(request.POST, request=request)
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 return redirect('/')
#             self.context = {
#                 'login_form': self.f_login(),
#                 'signup_form': list(form),
#             }
#         return render(request, self.template_name, self.context)

# @method_decorator(login_required(login_url='accounts/login'), name='dispatch')
# class Exit(TemplateView):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('/')

# @method_decorator(login_required(login_url='accounts/login'), name='dispatch')
# class PersonalInfo(TemplateView):
#     form_class = ProfileForm
#     context = {}
#     template_name = 'profile.html'

#     def get(self, request, *args, **kwargs):
#         user_id = request.user.id
#         print(user_id)
#         try:
#             self.context = {
#                 'user_info': UserInfo.objects.get(user=user_id),
#                 'user_recipes': UserRecipe.objects.filter(created_by=user_id),
#             }
#         except Exception as e:
#             print("self.context")
#             messages.error(request, message=e)
#         return render(request, self.template_name, self.context)

#     def post(self, request, *args, **kwargs):
#         pass