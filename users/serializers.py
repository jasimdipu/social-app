from rest_framework import serializers
from .models import UserModel, ProfileModel


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = "__all__"
