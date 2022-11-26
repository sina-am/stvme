# Generated by Django 4.1.2 on 2022-11-26 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='max_charge',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Maximum charge per word', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='max_time',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Maximum time per 5000 word in hour', null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='min_charge',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Minimum charge per word', max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='min_time',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Minimum time per 5000 word in hour', null=True),
        ),
    ]
