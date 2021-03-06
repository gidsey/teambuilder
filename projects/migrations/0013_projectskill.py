# Generated by Django 3.0.7 on 2020-07-01 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_portfolio'),
        ('projects', '0012_auto_20200629_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_skill', to='projects.Project')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_project', to='accounts.Skill')),
            ],
        ),
    ]
