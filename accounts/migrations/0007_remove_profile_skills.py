# Generated by Django 3.0.6 on 2020-05-30 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userskill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='skills',
        ),
    ]
