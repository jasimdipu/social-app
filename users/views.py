from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .serializers import ProfileSerializer
from .models import ProfileModel


# Create your views here.

class UserProfileViewSet(ModelViewSet):
    queryset = ProfileModel
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
