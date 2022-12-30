from django.contrib import admin
from .models import UserInfo, Post, Message, SavedPost, LikesPost

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    pass

@admin.register(LikesPost)
class LikesPostAdmin(admin.ModelAdmin):
    pass