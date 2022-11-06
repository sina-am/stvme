# Generated by Django 4.1.2 on 2022-11-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(choices=[('INVALID_ORDER', 'invalid order'), ('ESTIMATING_PRICE', 'waiting for estimation'), ('WAITING', 'waiting for accept')], max_length=20)),
                ('type', models.CharField(choices=[('EDIT', 'Edit'), ('TRANSLATION', 'Translation'), ('BOTH', 'Both')], max_length=12)),
                ('specialized_field', models.ManyToManyField(to='account.specializedfield')),
            ],
        ),
    ]
