from django.contrib.auth.models import User
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.db.models import Q


from .models import UserInfo, Post, Security, Follower
from .utils import *


import random # For later use, that we will randomize the Followed User list
# TODO: return a list of post that admin post, sort by country and try to implement the search ability to the search bar
################################

def home(request):
    context = {}
    template_name = 'index.html'
    
    # ALL OF THE POST THAT ALL USER HAVE MADE
    ALL_POST = Post.objects.all().order_by('-created')[:12] # only the first 12 posts 
    CHOSEN_USER = random.choice(User.objects.all())
    FAVORITE_USER_POST = Post.objects.filter(chef=CHOSEN_USER).order_by('-created')    
    context = {
        'user': request.user if request.user.is_authenticated else None,
        'FAVORITE_USER_POST': FAVORITE_USER_POST,
        'CHOSEN_USER': CHOSEN_USER,
        'ALL_POST': ALL_POST,
    }
    return render(request, template_name, context)


def search_post(request):
    """Search for a recipe

    Args:
        request (request): request object

    Returns:
        render: render template
    """
    
    context = {}
    
    if request.method == "GET":
        q = request.GET.get('header-search', '') + request.GET.get('search-main', '')
        
        if q == '':
            result_post = Post.objects.all().order_by('-created')
            q = 'All post created'
        else:
            result_post = Post.objects.filter(
                    Q(title__icontains = q) | 
                    Q(description__icontains = q)
                ).order_by('-created')
            
        result_amount = len(result_post)
        context = context | {
            'q': q,
            'result_amount': result_amount,
            'result_post': result_post,
        }
            
        
    template_name = "search.html"
    return render(request, template_name, context)


def post_detail(request, pk):
    context = {}
    template_name = 'view-post-details.html'
    try:
        recipe_post = Post.objects.get(pk=pk)
        recipe_post.ingredients = recipe_post.ingredients.split('\n')
        recipe_post.instructions = recipe_post.instructions.split('\n')
    except User.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        #Maybe post comments and likes
        pass
    context = {
        'post': recipe_post,
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
        Security.objects.create(
            user=user,
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
    if request.user.is_authenticated == True:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username-input').strip()
        password = request.POST.get('password-input').strip()
        context = {
            'username': username,
        }

        user = authenticate(request, username=username, password=password)
        if user:
            if user.security.two_step:
                verify_code = generate_verification_code()
                send_verification_code(to_email=user.email, code=verify_code)
                request.session['verify_code'] = verify_code
                request.session['verify_email'] = user.email
                return redirect('verify')
            login(request, user)
            return redirect('/')

        messages.error(request, "Email or Password is incorrect.")
        
    return render(request, template_name, context)

@login_required(login_url='login')
def logout_acc(request):
    logout(request)
    return redirect('/')


def verify_acc(request):
    context = {}
    template_name = 'twostep.html'
    input_code = None
    verify_code = request.session['verify_code']
    verify_email = request.session['verify_email']
    if request.method == 'POST':
        if 'resend' in request.POST:
            verify_code = generate_verification_code()
            send_verification_code(to_email=verify_email, code=verify_code)
            request.session['verify_code'] = verify_code
            messages.info(request, "We have resent the verification code.")
        else:
            input_code = request.POST.get('reset-code').strip()
            if input_code == verify_code:
                login(request, User.objects.get(email=verify_email))
                return redirect('/')
            messages.error(request, "The verification code you entered is incorrect.")

    context = {
        'input_code': input_code,
        'input_email': verify_email,
    }
    return render(request, template_name, context)

    
@login_required(login_url='login')
def profile_acc(request, pk): # pk username
    
    context = {}
    template_name = 'profile.html'
    # Request.user is the user that logged in, there for the profile information take the parameter from the urls to show it.
    try:
        user_info = User.objects.get(username=pk).userinfo
    except User.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        print(request.POST.keys())
        new_fullname = request.POST.get('fullname-input')
        new_password = request.POST.get('newpassword')
        new_avatar = request.FILES.get('img-profile')
        new_gender = request.POST.get('gender')
        new_2step = request.POST.get('enable-2factor')
        new_phone = request.POST.get('phone')
        new_bday = request.POST.get('birthday')
        new_bio = request.POST.get('bio-input')
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
        if new_bio:
            user_info.bio = new_bio.strip()
        if new_2step:
            user_info.user.security.two_step = True
            #(new_2step == "on")
        else:
            user_info.user.security.two_step = False
        user_info.user.security.save(update_fields=['two_step'])
        user_info.save(update_fields=['fullname', 'avatar', 'gender', 'phone', 'bday', 'bio'])
        
        if request.POST.get('follow'):
            try:
                status = Follower.objects.get(user=user_info.user, user_followers=request.user)
            except Follower.DoesNotExist:
                status = None
            if not status:
                Follower.objects.create(
                    user=user_info.user, 
                    user_followers=request.user
                )
            else:
                status.delete()
        
    
    current_info = UserInfo.objects.get(user=request.user)    
    
    
    context = {
        'current_info': current_info,
        'user_info': user_info,
        'user_post': Post.objects.filter(chef=User.objects.get(username=pk)).order_by('-created'),
    }
    
    if (current_info != user_info):
        try:
            status = Follower.objects.get(user=user_info.user, user_followers=request.user)
        except Follower.DoesNotExist:
            status = None
        
        context = context | {
            'follow_status': 'Follow' if not status else 'Unfollow'
        }
    print(Follower.objects.filter(user=user_info.user))
    context = context | {
        'following_list': Follower.objects.filter(user_followers=user_info.user),
        'follower_list': Follower.objects.filter(user=user_info.user),
    }
    return render(request, template_name, context)


"""PostARecipe Views

Returns:
"""
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
        
        title_recipe = request.POST.get("title-recipe")
        description_recipe = request.POST.get("description-recipe")
        recipe_ration = request.POST.get("recipe-ration")
        recipe_prep_time = request.POST.get("recipe-prep-time")
        
        total_ingredients = ''

        for i in range(MAX_NUMBER_INGREDIENTS):
            ingredient = request.POST.get(f'ingredient{i}')
            if ingredient:
                total_ingredients += f'Ingredient {i}: {ingredient}\n'
                
        total_instructions = ''
        for i in range(MAX_NUMBER_INSTRUCTIONS):
            instructions = request.POST.get(f'instruction{i}')
            if instructions:
                total_instructions += f'Step {i}: {instructions}\n'
                
        
        context = context | {
            'title_recipe': title_recipe,
            'description_recipe': description_recipe,
            'recipe_ration': recipe_ration,
            'recipe_prep_time': recipe_prep_time,
        }
        user = request.user
        preview = request.FILES.get("result-img")
        categories = request.POST.get("country")
        
        Post.objects.create(
            chef=user,
            categories=categories,
            title=title_recipe,
            description=description_recipe,
            ingredients=total_ingredients,
            instructions=total_instructions,
            ration=recipe_ration,
            preptime=recipe_prep_time,
            preview=preview,
        )
        
    
    template_name = "post_a_recipe.html"
    return render(request, template_name, context)



