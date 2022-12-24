from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages



from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


from .models import UserInfo, Post



# def login_user(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST.get('input')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)

#         context = {
#             'username': username,
#         }
#         print(username)
#         if user is None:
#             messages.error(request, 'invalid username or password')
#             return render(request, 'login_signup.html', context)
#         login(request, user)
#         return redirect('/') 
    
#     return render(request, 'login_signup.html', context)

# def signup_user(request):
#     context = {}
#     template_name = 'login_signup.html'
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         fullname = request.POST.get('fullname')
#         email = request.POST.get('email')
#         gender = 'C'
#         context = {
#             'username': username,
#             'fullname': fullname,
#             'email': email,
#             'gender': gender,
#         }
#         print(username, password1, password2, fullname, email, gender)
        
        
#         if (password1 != password2):
#             messages.error(request, 'passwords do not match')
            
#             return render(request, template_name, context)

#         user = User.objects._user(username=username, password=make_password(password1), email=email)
        
#         user_info = UserInfo.objects.create(user=user, fullname=fullname, gender=gender[0])
#         login(request, user)
#         return redirect('/')
    
#     return render(request, template_name, context)
    
        
def home(request):
    context = {}
    template_name = 'index.html'
    try:
        user = UserInfo.objects.get(user=request.user)
    except :
        user = None
    context = {
        'user': user,
    }
    return render(request, template_name, context)

def signup_acc(request):
    # if user already logged in, they will go back to home-page
    if request.session.session_key is not None:
        return redirect('/')
    context = {}
    template_name = 'signup.html'

    if request.method == 'POST':
        fullname = request.POST.get('fullname-signup-input').strip()
        email = request.POST.get('email-signup-input').strip()
        username = request.POST.get('username-signup-input').strip()
        password1 = request.POST.get('password-signup-input').strip()
        password2 = request.POST.get('repassword-signup-input').strip()
        gender = request.POST.get('gender')
        
        context = {
            'fullname': fullname,
            'email': email,
            'username': username,
        }
        
        # Case: Signup Information Validation
        dup_username = User.objects.filter(username=username)
        dup_email = User.objects.filter(email=email)
        if dup_email or dup_username or password1 != password2:
            if password1 != password2:
                messages.error(request, "Confirm password does not match.")
            if dup_username:
                messages.error(request, "Username was already taken.")
            if dup_email:
                messages.error(request, "Email was already signed up.")
            return render(request, template_name, context)

        user = User.objects.create(
            username=username,
            password=make_password(password1),
            email=email,
        )
        UserInfo.objects.create(
            user=user,
            fullname=fullname,
            gender=gender,
        )

        login(request, user)
        return redirect('/')
        
    return render(request, template_name, context)


def login_acc(request):
    context = {}
    template_name = 'login.html'
    
    # if user already logged in, they will go back to home-page
    if request.session.session_key is not None:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username-input').strip()
        password = request.POST.get('password-input').strip()
        context = {
            'username': username,
        }

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')

        messages.error(request, "Email or Password is incorrect.")
        
    return render(request, template_name, context)

@login_required(login_url='login')
def rspw_acc(request):
    context = {}
    template_name = 'forgot_password.html'
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email):
            return redirect('password_reset_confirm')

        messages.error(request, "Email has not been signed up.")
        context = {
            'email': email,
        }
    return render(request, template_name, context)


@login_required(login_url='login')
def rspw_acc_cf(request):
    context = {}
    template_name = 'forgot_password1.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def rspw_acc_done(request):
    context = {}
    template_name = 'forgot_password2.html'
    return render(request, template_name, context)

@login_required(login_url='login')
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')

@login_required(login_url='login')
def logout_acc(request):
    logout(request)
    return redirect('/')
    
@login_required(login_url='login')
def profile_acc(request):
    """ TODO: Saved recipes, My Posts
    """
    context = {}
    template_name = 'profile.html'
    user_info = UserInfo.objects.get(user=request.user)

    if request.method == 'POST':
        new_fullname = request.POST.get('fullname-input')
        new_password = request.POST.get('newpassword')
        new_avatar = request.FILES.get('img-profile')
        new_gender = request.POST.get('gender')
        new_phone = request.POST.get('phone')
        new_bday = request.POST.get('birthday')

        # Case: Compare old and new password
        if new_password:
            new_password = new_password.strip()
            if user_info.user.check_password(new_password):
                messages.error(request, "New password cannot be the same as your old password.")
            else:
                user_info.user.set_password(new_password)
                user_info.user.save()
        if new_fullname:
            user_info.fullname = new_fullname.strip()
        if new_avatar:
            user_info.avatar = new_avatar
        if new_gender:
            user_info.gender = new_gender
        if new_phone:
            user_info.phone = new_phone.strip()
        if new_bday:
            user_info.bday = new_bday
        
        user_info.save(update_fields=['fullname', 'avatar', 'gender', 'phone', 'bday'])

    context = {
        'user_info': user_info,
    }
    return render(request, template_name, context)

@login_required(login_url='login')
def PostARecipe(request):
    # TODO: make a Post Model to create a Post that made by a User
    
    user_info = UserInfo.objects.get(user=request.user)
    context = {
        'user_info': user_info,
    }
    if (request.method == 'POST'):
        ar = request.POST.keys()
        
        new_title_recipe = request.POST["title-recipe"]
        new_description_recipe = request.POST["description-recipe"]
        new_recipe_ration = request.POST["recipe-ration"]
        new_recipe_prep_time = request.POST["recipe-prep-time"]
        
        new_ingredient0 = request.POST["ingredient0"]
        new_ingredient1 = request.POST["ingredient1"]
        new_instruction0 = request.POST["instruction0"]
        new_instruction1 = request.POST["instruction1"]
        
        new_result_img = request.FILES["result-img"]
        new_country = request.POST["country"]
        for key in ar:
            # print(f"if new_{key}:")

            print(f"\tnew_{key.replace('-', '_')} = request.POST.get(\"{key}\")")
        pass
    
    template_name = "post_a_recipe.html"
    return render(request, template_name, context)