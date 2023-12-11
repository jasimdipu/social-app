from django.urls import include, path
from . import views

urlpatterns = [
    path("friends-list", views.FriendListView.as_view()),
    path("friends-requests", views.FriendRequestsListView.as_view()),
    path("send-friends-requests/<str:username>", views.FriendshipRequestViewSet.as_view()),
    path("accept-friends-requests/<str:username>", views.AcceptFriendRequestViewSet.as_view()),
    path("friends-of-friends", views.FriendsOfFriendListView.as_view()),
    path("mutual-friends", views.MutualFriendListView.as_view()),
    path("friend-ship-status/<str:username1>/<str:username2>", views.FriendshipStatusListView.as_view()),
]
