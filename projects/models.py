from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """"
    Model to hold the Project data.
    """
    owner = models.ForeignKey(User, related_name='owner_project', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timeline = models.TextField(blank=True)
    requirements = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Position(models.Model):
    """
    Holds the positions linked to projects.
    """
    project = models.ForeignKey(Project, related_name='positions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
