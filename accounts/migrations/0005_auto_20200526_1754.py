# Generated by Django 3.0.6 on 2020-05-26 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_skill_userskill'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.DeleteModel(
            name='UserSkill',
        ),
    ]