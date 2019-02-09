from django.db import models
#from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import UsernameValidator
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class ClientList(models.Model):
    client_name = models.CharField(max_length=150)
    client_company = models.CharField(max_length=150)
    company_location = models.CharField(max_length=50, blank=False)
    company_logo = models.ImageField(upload_to = 'media/img/', default = 'media/no-image.png',blank=True,null=True)
    contactno = models.CharField(max_length=20, blank=False)
    project_name = models.CharField(max_length=100, blank=False)
    tools = models.CharField(max_length=100, blank=False)
    offer_date = models.CharField(max_length=150)
    deadline =  models.CharField(max_length=150)

    def __str__(self):
        return self.client_name



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have a valid email address.")

        # if not phonenumber:
        #     raise ValueError("User must have a valid phonenumber.")

        if not kwargs.get('username'):
            raise ValueError('User must have a valid username')

        user = self.model(
            username=kwargs.get('username').strip(),
            email=self.normalize_email(email),
            # phonenumber = phonenumber,
            first_name=kwargs.get('first_name', None),
            last_name=kwargs.get('last_name', None),
            # is_confirmed=kwargs.get('is_confirmed', False),
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, is_staff=True, **kwargs):
        user = self.create_user(email, password,**kwargs)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[UsernameValidator()],
        error_messages={
            'unique': 'User with this username already exists.',
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'User with this email already exists.',
        },
    )
    # phonenumber = models.CharField(
    #     max_length=15,
    #     unique=True,
    #     validators=[PhoneNumberValidator()],
    #     error_messages={
    #         'unique': 'User with this phonenumber already exists.',
    #     },


    # )
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        "does the user have the special permission?"
        #simplest possible answer: yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # simplest possible answers: All admins are staff
        return self.is_admin


    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    # def __str__(self):
    #     return self.phonenumber

    class Meta:
        db_table = "users"
