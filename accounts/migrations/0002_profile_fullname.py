# Generated by Django 3.0.6 on 2020-05-09 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fullname',
            field=models.CharField(default='fullname', max_length=255),
            preserve_default=False,
        ),
    ]
