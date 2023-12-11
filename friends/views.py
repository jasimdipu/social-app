import json

from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users.models import UserModel
from .models import Friend, FriendshipRequest
from .serializers import FriendSerializer, FriendshipRequestSerializer, FriendshipStatusSerializer, \
    UserModelSerializer


class FriendListView(generics.ListAPIView):
    """
    List a user's friends.

    This view allows an authenticated user to retrieve a list of their friends.

    Response Example:
    ---
    A successful response will include a list of friend objects. Each friend object contains the following fields:

    - `id`: Unique identifier for the friend relationship.
    - `to_user`: The user to whom the authenticated user is friends with.
    - `from_user`: The authenticated user who is friends with another user.

    Response:
    [
        {
            "id": 1,
            "to_user": {
                "id": 2,
                "username": "friend1"
            },
            "from_user": {
                "id": 1,
                "username": "authenticated_user"
            }
        },
        {
            "id": 2,
            "to_user": {
                "id": 3,
                "username": "friend2"
            },
            "from_user": {
                "id": 1,
                "username": "authenticated_user"
            }
        }
    ]
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Utilize the existing `friends` method from the manager
        friends = Friend.objects.friends(user)

        return friends


class FriendRequestsListView(generics.ListAPIView):
    """
        List a user's friendship requests.

        This view allows an authenticated user to retrieve a list of their friendship requests.

        Permissions:
        - User must be authenticated.

        Request Example:
        ---
        No request parameters are required. The endpoint is accessible to authenticated users.

        A successful response will include a list of friend objects. Each friend object contains the following fields:

        - `id`: Unique identifier for the friend relationship.
        - `to_user`: The user to whom the authenticated user is friends with.
        - `from_user`: The authenticated user who is friends with another user.

        Example Response:
        [
            {
                "id": 1,
                "from_user": {
                    "id": 2,
                    "username": "friend1"
                },
                "to_user": {
                    "id": 1,
                    "username": "authenticated_user"
                }
            },
            {
                "id": 2,
                "from_user": {
                    "id": 3,
                    "username": "friend2"
                },
                "to_user": {
                    "id": 1,
                    "username": "authenticated_user"
                }
            }
        ]
    """
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the authenticated user
        user = self.request.user

        # Utilize the existing `friends` method from the manager
        friends = Friend.objects.requests(user)

        return friends


class FriendshipRequestViewSet(generics.CreateAPIView):
    """
        Create a friendship request.

        This view allows authenticated users to send friend requests to other users.

        Parameters:
        - `username` (str): The username of the user you want to send a friend request to.

        Returns:
        - 201 Created: If the friend request is successfully sent.
        - 400 Bad Request: If there is an issue with the request, such as an invalid username or an error in creating the request.
    """
    queryset = FriendshipRequest
    serializer_class = FriendshipRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username=None, *args, **kwargs):
        if username is not None:
            friend_user = UserModel.objects.get(username=username)
            try:
                friend_request = Friend.objects.add_friend(request.user, friend_user,
                                                           message='Hi! I would like to add you')
            except Exception as e:
                data = {
                    'status': False,
                    'message': str(e),
                }
                return JsonResponse(data)

            data = {
                'status': True,
                'message': "Request sent.",
                'friend_request': FriendshipRequestSerializer(friend_request).data,
            }
            return JsonResponse(data)
        else:
            return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestViewSet(generics.CreateAPIView):
    """
        Accept a friend request.

        This view allows authenticated users to accept a friend request from another user.

        Parameters:
        - `username` (str): The username of the user whose friend request you want to accept.

        Returns:
        - 200 OK: If the friend request is successfully accepted.
        - 400 Bad Request: If there is an issue with the request, such as an invalid username or if the friend request does not exist.
        """
    queryset = FriendshipRequest
    serializer_class = FriendshipRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username=None, *args, **kwargs):
        if username is not None:
            friend_user = UserModel.objects.get(username=username)
            try:
                friend_request = FriendshipRequest.objects.get(to_user=request.user, from_user=friend_user)
                friend_request.accept()
                data = {
                    'status': True,
                    'message': "You accepted the friend request",
                }
                return JsonResponse(data)
            except FriendshipRequest.DoesNotExist:
                return JsonResponse({'detail': 'Friend request not found.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)


class MutualFriendListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get the friends of the user
        friends = Friend.objects.friends(user)

        # Get friends of your friends (including your friends)
        friends_of_friends = Friend.objects.filter(to_user__in=friends)

        return friends_of_friends


class FriendsOfFriendListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get the friends of the user
        friends = Friend.objects.friends(user)

        # Get friends of your friends (including your friends)
        friends_of_friends = Friend.objects.filter(to_user__in=friends)

        return friends_of_friends


class FriendshipStatusListView(generics.ListAPIView):
    """
        Provides the friendship status and mutual friends list between two users.

        This view allows you to check if two users are friends and, if not, it returns a list of mutual friends if they
         are connected through other users.

        ---
        **parameters**
            -- name: username1
              description: The username of the first user.
              required: true
              type: string
              paramType: query
            -- name: username2
              description: The username of the second user.
              required: true
              type: string
              paramType: query
        **responses**
            200:
                description: Friendship status and list of mutual friends.
            400:
                description: Bad request, e.g., when a user is not found.
        """

    serializer_class = FriendshipStatusSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username1 = self.kwargs.get('username1', None)
        username2 = self.kwargs.get('username2', None)

        if not username1 or not username2:
            return Response({'detail': 'Please provide both usernames.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user1 = UserModel.objects.get(username=username1)
            user2 = UserModel.objects.get(username=username2)

            # Check if the two users are already friends
            if Friend.objects.are_friends(user1, user2):
                friends_list = Friend.objects.friends(user1)
                response_data = {
                    "friendship_status": "Friends",
                    "friends_or_mutual": friends_list,
                }
            else:
                # Find mutual friends
                mutual_friends = self.get_mutual_friends(user1, user2)
                response_data = {
                    "friendship_status": "Not Friends",
                    "friends_or_mutual": mutual_friends,
                }

            serializer = FriendshipStatusSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    def get_mutual_friends(self, user1, user2):
        friends_user1 = set(Friend.objects.friends(user1))
        friends_user2 = set(Friend.objects.friends(user2))
        mutual_friends = friends_user1.union(friends_user2)

        # Iterate through mutual friends to find all mutual connections
        all_mutual_connections = [user1, user2]
        for friend in mutual_friends:
            if friend != user1 and friend != user2:
                all_mutual_connections.append(friend)

        return all_mutual_connections
