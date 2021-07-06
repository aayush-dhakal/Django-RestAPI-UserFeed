from django.db import models
# imports required to override default django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    # when a function is defined inside of a class then its first parameter must be self but when you call a class's function self parameter is automatically passed
    def create_user(self,email,name,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)  # email normalization basically turns second half of an email(ie after @ part) into lowercase. eg: normalize_email("user@EXAMPLE.COM"") gives user@example.com

        user = self.model(email=email, name=name) # this creates a new user model object

        user.set_password(password)  # set_password method encrypts the password

        user.save(using=self._db) # self._db saves the user in django's default user table. you can also use multiple tables

        return user  # returns newly created user


    def create_superuser(self,email,name,password):
        """Create and save a new superuser with given details"""

        # we are using method of a class so access it by using self(similar to 'this' method in other languages)
        user = self.create_user(email, name, password) # when you call a class's function self parameter is automatically passed

        # PermissionsMixin automatically created is_superuser for us
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=225,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # staff users will be able to access admin panel

    objects = UserProfileManager()

    # by default django logs in with username. so here this code overrides that property to login with email instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        # refer this to understand __str__ usage
        # https://www.youtube.com/watch?v=khdVg1lLbZo&ab_channel=GeekyShows  or 
        #  https://stackoverflow.com/questions/45483417/what-is-doing-str-function-in-django

        # The __str__ method just tells Django what to print when it needs to print out an instance of the any model. It is also what lets your admin panel to be more human readable ie the column of user data will show the email of the user and therefore will be easier to identify. By default it will show as User object(1) form
        # also make sure the field you are providing is in string form. If it is in another form then you need to conver the result in string form using str() method 
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, # best pratice is to link the model from the settings file instead of hardcoding the model name in string
        # when the user profile is deleted then we also want their feeds to be deleted
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
