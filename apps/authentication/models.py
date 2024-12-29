from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group, Permission

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, username: str, password: str, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, username: str, password: str=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email: str, username: str, password: str):
        user = self.create_user(email, username, password)
        user.staff = True
        user.active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, null=False, blank=False, unique=True)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. '\
                                                         'Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    @property
    def is_staff(self):
        return self.staff

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
