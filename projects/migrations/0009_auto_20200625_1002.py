# Generated by Django 3.0.7 on 2020-06-25 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0008_auto_20200624_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapplication',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_position', to='projects.Position'),
        ),
        migrations.AlterField(
            model_name='userapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
