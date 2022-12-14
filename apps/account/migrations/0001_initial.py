# Generated by Django 4.1.2 on 2022-12-14 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('EDITOR', 'editor'), ('TRANSLATOR', 'translator'), ('CUSTOMER', 'customer')], default='CUSTOMER', max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_charge', models.DecimalField(blank=True, decimal_places=2, help_text='Minimum charge per word', max_digits=10, null=True)),
                ('max_charge', models.DecimalField(blank=True, decimal_places=2, help_text='Maximum charge per word', max_digits=10, null=True)),
                ('max_time', models.PositiveSmallIntegerField(blank=True, help_text='Maximum time per 5000 word in hour', null=True)),
                ('min_time', models.PositiveSmallIntegerField(blank=True, help_text='Minimum time per 5000 word in hour', null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('languages', models.ManyToManyField(help_text='languages that you know', related_name='employee_languages', to='common.language', verbose_name='languages')),
                ('specialized_fields', models.ManyToManyField(help_text='your professional fields', related_name='employee_fields', to='common.specializedfield')),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.AddConstraint(
            model_name='employee',
            constraint=models.CheckConstraint(check=models.Q(('min_charge__lt', models.F('max_charge'))), name='min charge should be less than max charge'),
        ),
        migrations.AddConstraint(
            model_name='employee',
            constraint=models.CheckConstraint(check=models.Q(('min_time__lt', models.F('max_time'))), name='min time should be less than max time'),
        ),
    ]
