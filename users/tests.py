from django.test import TestCase
from .models import ProfileModel, UserModel


class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            gender="male",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.get_full_name(), "Test User")
        self.assertEqual(self.user.gender, "male")

    def test_user_str(self):
        self.assertEqual(str(self.user), "Test User")


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            gender="male",
        )
        self.profile = ProfileModel.objects.create(
            user=self.user,
            profile_image="avatars/test_profile.jpg",
            cover_image="avatars/test_cover.jpg",
            phone="1234567890",
            city="Test City",
            country="Test Country",
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.profile_image, "avatars/test_profile.jpg")
        self.assertEqual(self.profile.cover_image, "avatars/test_cover.jpg")
        self.assertEqual(self.profile.phone, "1234567890")
        self.assertEqual(self.profile.city, "Test City")
        self.assertEqual(self.profile.country, "Test Country")

    def test_get_profile_image(self):
        self.assertEqual(self.profile.get_profile_image(), "avatars/test_profile.jpg")

    def test_get_cover_image(self):
        self.assertEqual(self.profile.get_cover_image(), "avatars/test_cover.jpg")
