from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import UserModel
from friends.models import FriendshipRequest, Friend


class FriendshipRequestTest(TestCase):
    def test_accept_request(self):
        # Create two users
        user1 = UserModel.objects.create(username="user1")
        user2 = UserModel.objects.create(username="user2")

        # Create a friendship request from user1 to user2
        request = FriendshipRequest.objects.create(from_user=user1, to_user=user2)

        # Accept the request
        request.accept()

        # Check if a friendship has been created
        self.assertTrue(Friend.objects.are_friends(user1, user2))

    def test_cancel_request(self):
        user1 = UserModel.objects.create(username="user1")
        user2 = UserModel.objects.create(username="user2")
        request = FriendshipRequest.objects.create(from_user=user1, to_user=user2)

        # Cancel the request
        request.cancel()

        # Check if the request has been deleted
        self.assertFalse(FriendshipRequest.objects.filter(id=request.id).exists())

    def test_mark_request_viewed(self):
        user1 = UserModel.objects.create(username="user1")
        user2 = UserModel.objects.create(username="user2")
        request = FriendshipRequest.objects.create(from_user=user1, to_user=user2)

        # Mark the request as viewed
        request.mark_viewed()

        # Check if the request has been marked as viewed
        self.assertIsNotNone(request.viewed)

    def setUp(self):
        # Create two unique users with different usernames and emails
        self.user1 = UserModel.objects.create(username="user1", email="user1@example.com")
        self.user2 = UserModel.objects.create(username="user2", email="user2@example.com")

    def test_reject_request(self):
        # Create a friendship request from user1 to user2
        request = FriendshipRequest.objects.create(from_user=self.user1, to_user=self.user2)

        # Reject the request
        request.reject()

        # Check if the request has been rejected
        self.assertIsNotNone(request.rejected)


class FriendTest(TestCase):
    def test_create_friendship(self):
        user1 = UserModel.objects.create(username="user1")
        user2 = UserModel.objects.create(username="user2")

        # Create a friendship between user1 and user2
        friend = Friend.objects.create(to_user=user1, from_user=user2)

        # Check if the friendship has been created
        self.assertTrue(Friend.objects.are_friends(user1, user2))

    def test_cannot_be_friends_with_self(self):
        user = UserModel.objects.create(username="user")

        # Try to create a friendship with oneself
        with self.assertRaises(ValidationError):
            Friend.objects.create(to_user=user, from_user=user)
