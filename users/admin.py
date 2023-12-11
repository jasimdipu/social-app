from django.contrib import admin
from .models import UserModel, ProfileModel


# Register your models here.

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_active']


@admin.register(ProfileModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_image', 'phone', 'city', 'country']
