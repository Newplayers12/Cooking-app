from django.contrib.auth.models import User
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from .models import UserInfo, Post
    
        
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

    user_post = Post.objects.filter(chef=request.user)
    context = {
        'user_info': user_info,
        'user_post': user_post,
    }
    return render(request, template_name, context)


MAX_NUMBER_INGREDIENTS = 10
MAX_NUMBER_INSTRUCTIONS = 10
@login_required(login_url='login')
def PostARecipe(request):
    # TODO: make a Post Model to create a Post that made by a User
    
    user_info = UserInfo.objects.get(user=request.user)
    context = {
        'user_info': user_info,
    }
    if (request.method == 'POST'):
        ar = request.POST.keys()
        
        new_title_recipe = request.POST.get("title-recipe")
        new_description_recipe = request.POST.get("description-recipe")
        new_recipe_ration = request.POST.get("recipe-ration")
        new_recipe_prep_time = request.POST.get("recipe-prep-time")
        
        # new_ingredient0 = request.POST.get("ingredient0")
        # new_ingredient1 = request.POST.get("ingredient1")
        total_ingredients = ''
        total_instructions = ''
        for i in range(MAX_NUMBER_INGREDIENTS):
            line =  request.POST.get(f"ingredient{i}")
            if line:
                total_ingredients += line
                total_ingredients += '\n'

        for i in range(MAX_NUMBER_INSTRUCTIONS):
            line = request.POST.get(f"instruction{i}")
            if line:
                total_instructions += line
                total_instructions += '\n'
        
        # new_instruction0 = request.POST.get("instruction0")
        # new_instruction1 = request.POST.get("instruction1")
        
        new_result_img = request.FILES.get("result-img")
        new_country = request.POST.get("country")
        
        Post.objects.create(
            chef=request.user,
            categories = new_country,
            title = new_title_recipe,
            description = new_description_recipe,
            ration = new_recipe_ration,
            preptime = new_recipe_prep_time,
            ingredients = total_ingredients,
            instructions = total_instructions,
            preview = new_result_img
        )
        
        
    
    template_name = "post_a_recipe.html"
    return render(request, template_name, context)