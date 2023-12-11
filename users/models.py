from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import BaseModel


class UserModel(AbstractUser, BaseModel):
    GENDER_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),
    )
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    gender = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    about = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "gender"]

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.get_full_name()


class ProfileModel(BaseModel):
    user = models.OneToOneField(UserModel, on_delete=models.DO_NOTHING, related_name='profile')
    profile_image = models.ImageField(upload_to='avatars', default='avatars/guest.png')
    cover_image = models.ImageField(upload_to='avatars', default='avatars/cover.png')
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return settings.MEDIA_URL + self._meta.get_field('profile_image').get_default()

    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image.url
        return settings.MEDIA_URL + self._meta.get_field('cover_image').get_default()


@receiver(post_save, sender=UserModel)
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        ProfileModel.objects.create(user=kwargs['instance'])
