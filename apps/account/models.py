from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    """ Languages that are supported for translation source and target"""
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'languages'

    def __str__(self):
        return self.name

    
class SpecializedField(models.Model):
    """ Specialized fields for employee who translate text"""
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'specialized_fields'

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """ Manager for user profiles """
    def create_permissions(self, user):
        if user.is_customer:
            group, created = Group.objects.get_or_create(name='customers')
            user.groups.add(group)
        elif user.is_employee:
            group, created = Group.objects.get_or_create(name='employees')
            user.groups.add(group)

    def create_user(self, email, first_name, last_name, password=None, role='CUSTOMER'):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        self.create_permissions(user)
        
        if user.role in User.EMPLOYEE_ROLES:
            Employee.objects.create(user=user)
            
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
    
    EDITOR_ROLE = "EDITOR"
    TRANSLATOR_ROLE = "TRANSLATOR"
    CUSTOMER_ROLE = "CUSTOMER"
    
    EMPLOYEE_ROLES = (
        (EDITOR_ROLE, _('editor')),
        (TRANSLATOR_ROLE, _('translator')),
    )
    ROLES = (
        (EDITOR_ROLE, _('editor')),
        (TRANSLATOR_ROLE, _('translator')),
        (CUSTOMER_ROLE, _('customer')),
    )

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(choices=ROLES, max_length=10, default=CUSTOMER_ROLE)
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
    def is_employee(self):
        return self.role in [self.EDITOR_ROLE, self.TRANSLATOR_ROLE]
    
    @property
    def is_customer(self):
        return self.role == self.CUSTOMER_ROLE
            
    
class Employee(models.Model):
    """ Translators and editors model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, related_name='employee_languages')
    specialized_fields = models.ManyToManyField(SpecializedField, related_name='employee_fields')
    min_charge = models.DecimalField(max_digits=10, decimal_places=2, help_text='Minimum charge per word', null=True, blank=True)
    max_charge = models.DecimalField(max_digits=10, decimal_places=2, help_text='Maximum charge per word', null=True, blank=True)
    max_time = models.PositiveSmallIntegerField(help_text='Maximum time per 5000 word in hour', null=True, blank=True)
    min_time = models.PositiveSmallIntegerField(help_text='Minimum time per 5000 word in hour', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'employees'
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