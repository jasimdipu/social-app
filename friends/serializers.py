from rest_framework import serializers
from .models import Friend, FriendshipRequest
from users.models import UserModel, ProfileModel


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('profile_image', 'phone', 'city', 'country')


class UserModelSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(source='profile.profile_image', read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    country = serializers.CharField(source='profile.country', read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'profile_image', 'phone', 'city', 'country')


class FriendSerializer(serializers.ModelSerializer):
    to_user_info = UserModelSerializer(source='to_user', read_only=True)
    from_user_info = UserModelSerializer(source='from_user', read_only=True)

    class Meta:
        model = Friend
        fields = ('id', 'to_user_info', 'from_user_info')


class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user_info = UserModelSerializer(source='from_user', read_only=True)
    to_user_info = UserModelSerializer(source='to_user', read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user_info', 'to_user_info', 'message', 'rejected', 'viewed')


class FriendshipStatusSerializer(serializers.Serializer):
    friendship_status = serializers.CharField()
    friends_or_mutual = UserModelSerializer(many=True)

    def get_friends_or_mutual(self, obj):
        return obj['friends_or_mutual']
