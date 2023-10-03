# Generated by Django 4.2.5 on 2023-10-03 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_mfa', '0002_userprofile_mfa_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mfa_method',
            field=models.CharField(choices=[('TOTP', 'TOTP'), ('SMS', 'SMS')], max_length=4),
        ),
    ]