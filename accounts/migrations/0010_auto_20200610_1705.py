# Generated by Django 3.0.7 on 2020-06-10 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200610_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(default='j', max_length=255),
            preserve_default=False,
        ),
    ]