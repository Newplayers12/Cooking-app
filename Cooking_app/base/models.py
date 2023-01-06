from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models


# class FoodType(models.Model):
#     name = models.CharField(max_length=200)
#     def __str__(self):
#         return self.name

class Security(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    two_step = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Username = {self.user.username} and two factor activated = {self.two_step}"

class UserInfo(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Custom', 'Custom'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(blank=False, max_length=150, null=False)
    bio = models.TextField(blank=False, max_length=2000, null=True)
    gender = models.CharField(blank=False, choices=GENDER_CHOICES, max_length=6, null=True)
    phone = models.CharField(blank=False, max_length=20, null=True)
    avatar = models.ImageField(upload_to='personal_avatar', default="default_avatar.png")
    bday = models.DateField(blank=False, null=True)

    def __str__(self):
        return f"User fullname = {self.fullname}"

class Post(models.Model):
    CATEGORIES_CHOICES = (
        ('Vietnam', 'Vietnam'),
        ('Laos', 'Laos'),
        ('Cambodia', 'Cambodia'),
    )
    chef = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categories = models.CharField(blank=False, choices=CATEGORIES_CHOICES, max_length=100, null=True)
    
    title = models.CharField(blank=False, max_length=2000, null=True)
    description = models.TextField(blank=False, max_length=2000, null=True)
    ration = models.IntegerField(blank=False, null=True)
    preptime = models.IntegerField(blank=False, null=True)
    ingredients = models.TextField(blank=False, max_length=1000, null=True)
    instructions = models.TextField(blank=False, max_length=1000, null=True)
    preview = models.ImageField(upload_to='recipe_preview', default="default_recipe.jpg")
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Username = {self.chef.username} and title = {self.title}"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    body = models.TextField(blank=False, null=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # printing only the first 50 character of the message to preview.
        return self.body[:50]

## Saved Post and Likes Post models 

#### NOTE: This is not the same as the other models, it has different meaning
#### One for the saved Post of each user
class SavedPost(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Saved_post = models.OneToOneField(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
#### Other one for Liked Post of that user.
class LikesPost(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Liked_post = models.OneToOneField(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first")
    user_followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second")
     
    def __str__(self):
        return f"{self.user_followers.username} is following {self.user.username}"

""" class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breakfast = models.ForeignKey(Post, on_delete=models.CASCADE)
    lunch = models.ForeignKey(Post, on_delete=models.CASCADE)
    dinner = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.breakfast.title}, {self.lunch.title}, {self.dinner.title}"
"""