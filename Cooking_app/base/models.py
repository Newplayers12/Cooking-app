from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models


class FoodType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class UserInfo(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Custom', 'Custom'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(blank=False, max_length=150, null=False)
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
    categories = models.CharField(blank=False, choices=CATEGORIES_CHOICES, max_length=1000, null=True)
    
    title = models.CharField(blank=False, max_length=200, null=True)
    description = models.CharField(blank=False, max_length=200, null=True)
    ration = models.IntegerField(blank=False, null=True)
    preptime = models.IntegerField(blank=False, null=True)
    ingredients = models.CharField(blank=False, max_length=1000, null=True)
    instructions = models.CharField(blank=False, max_length=1000, null=True)
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
