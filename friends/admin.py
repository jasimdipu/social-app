from django.contrib import admin
from .models import Friend, FriendshipRequest


# Register your models here.

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['to_user', 'from_user']


@admin.register(FriendshipRequest)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']
