from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models



class FoodType(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    

class UserInfo(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custome'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(blank=False, max_length=150, null=False)
    gender = models.CharField(blank=False, choices=GENDER_CHOICES, max_length=1, null=True)
    phone = models.CharField(blank=False, max_length=20, null=True)
    avatar = models.ImageField(upload_to='personal_avatar', default="default_avatar.png")
    bday = models.DateField(blank=False, null=True)

    def __str__(self):
        return self.fullname

class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    food_type = models.ForeignKey(FoodType, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(blank=False, max_length=200, null=False)
    description = models.CharField(blank=False, max_length=200, null=False)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        
        
    def __str__(self):
        return str(self.name)
    


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    body = models.TextField(blank=False, null=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # printing only the first 50 character of the message to preview.
        return self.body[:50]
    
    
