from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from apps.common.models import Language, SpecializedField


class UserManager(BaseUserManager):
    """ Manager for user profiles """
    def create_permissions(self, user):
        if user.is_client:
            group, created = Group.objects.get_or_create(name='clients')
            user.groups.add(group)
        elif user.is_translator:
            group, created = Group.objects.get_or_create(name='translators')
            user.groups.add(group)

    def create_user(self, email, first_name, last_name, password=None, role='CLIENT'):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        self.create_permissions(user)
        
        if user.role == User.TRANSLATOR_ROLE:
            Translator.objects.create(user=user)
            
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

    TRANSLATOR_ROLE = "TRANSLATOR"
    CLIENT_ROLE = "CLIENT"
    
    ROLES = (
        (TRANSLATOR_ROLE, _('translator')),
        (CLIENT_ROLE, _('client')),
    )

    email = models.EmailField(max_length=255, unique=True, verbose_name=_('email'))
    first_name = models.CharField(max_length=255, verbose_name=_('first name'))
    last_name = models.CharField(max_length=255, verbose_name=_('last name'))
    role = models.CharField(choices=ROLES, max_length=10, default=CLIENT_ROLE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        """ Return string representation of our user """
        return self.email

    @property
    def is_translator(self):
        return self.role == self.TRANSLATOR_ROLE
    
    @property
    def is_client(self):
        return self.role == self.CLIENT_ROLE
            
    
class Translator(models.Model):
    """ Translators and editors model."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        editable=False
    )
    languages = models.ManyToManyField(
        Language,
        related_name='translator_languages', 
        help_text=_("languages that you know"),
        verbose_name=_("languages")
    )
    specialized_fields = models.ManyToManyField(
        SpecializedField,
        related_name='translator_fields',
        help_text=_("your professional fields")     
    )
    min_charge = models.DecimalField(max_digits=10, decimal_places=2, help_text='Minimum charge per word', null=True, blank=True)
    max_charge = models.DecimalField(max_digits=10, decimal_places=2, help_text='Maximum charge per word', null=True, blank=True)
    max_time = models.PositiveSmallIntegerField(help_text='Maximum time per 5000 word in hour', null=True, blank=True)
    min_time = models.PositiveSmallIntegerField(help_text='Minimum time per 5000 word in hour', null=True, blank=True)
    is_available = models.BooleanField(default=True, )

    credit = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'translators'
        constraints = [
            models.CheckConstraint(
                check=models.Q(min_charge__lt=models.F('max_charge')),
                name=_("min charge should be less than max charge"),
            ),
            models.CheckConstraint(
                check=models.Q(min_time__lt=models.F('max_time')),
                name=_("min time should be less than max time"),
            )
        ]