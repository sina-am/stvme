from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    """ Languages that are supported for translation source and target"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SpecializedField(models.Model):
    """ Specialized fields for employee who translate text"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, first_name, last_name, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """ Create a new superuser profile """
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    ROLES = (
        ('OPRATOR', _('oprator')),
        ('EDITOR', _('editor')),
        ('TRANSLATOR', _('translator')),
        ('CUSTOMER', _('customer')),
    )

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(choices=ROLES, max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """ Return string representation of our user """
        return self.email


class Employee(User):
    """ Translators and editors model."""
    languages = models.ManyToManyField(Language, related_name='employee_languages')
    specialized_field = models.ManyToManyField(SpecializedField, related_name='employee_fields')
    min_charge = models.DecimalField(max_digits=10, decimal_places=2, help_text='Minimum charge per word')
    max_charge = models.DecimalField(max_digits=10, decimal_places=2, help_text='Maximum charge per word')
    max_time = models.PositiveSmallIntegerField(help_text='Maximum time per 5000 word in hour')
    min_time = models.PositiveSmallIntegerField(help_text='Minimum time per 5000 word in hour')
    is_available = models.BooleanField(default=True)

    