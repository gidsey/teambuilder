from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from accounts.models import Skill

class Project(models.Model):
    """"
    Model to hold the Project data.
    """
    owner = models.ForeignKey(User, related_name='owner_project', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timeline = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Position(models.Model):
    """
    Holds the positions linked to projects.
    """
    project = models.ForeignKey(Project, related_name='positions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserApplication(models.Model):
    """
    Holds the applications for each position.
    Status can be:
    1 - undecided
    2 - approved
    3 - rejected

    """
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, related_name='application_position', on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)


class ProjectSkill(models.Model):
    """
    Add one or many skills to the project.
    """
    project = models.ForeignKey(Project, related_name='project_skill', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='skill_project', on_delete=models.CASCADE)