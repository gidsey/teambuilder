# Generated by Django 3.0.8 on 2020-07-10 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_portfolio'),
        ('projects', '0014_projectskill_required_skill'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='key_skill',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='key_skill', to='accounts.Skill'),
            preserve_default=False,
        ),
    ]