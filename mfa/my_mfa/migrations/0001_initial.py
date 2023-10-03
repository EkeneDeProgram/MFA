# Generated by Django 4.2.5 on 2023-09-26 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_key', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('mfa_enabled', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, help_text='Enter your phone number in the format: +2348155813450', max_length=13, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]