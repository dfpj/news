import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE,null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Verify(models.Model):
    email = models.EmailField()
    code = models.PositiveSmallIntegerField()
    send_date = models.DateTimeField(auto_now_add=True)
    allow_update_pass = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email}'

    def check_verify(self, user, code):
        time_accept = settings.TIME_VERIFY_CODE_SECOND
        if self.send_date + datetime.timedelta(seconds=time_accept) < now():
            return False
        else:
            if self.code == code:
                return True
            return False


class Profile(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    birthday = models.DateField(default=now)
    avatar = models.ImageField(default="1.jpg")
