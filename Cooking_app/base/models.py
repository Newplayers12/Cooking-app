from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models


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
# UserInfo(fullname=None, gender=None, phone=None, avatar=None, bday=None)
class UserRecipe(models.Model):
    pass