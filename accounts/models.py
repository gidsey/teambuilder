from django.db import models
from django.contrib.auth.models import User
from .utils import user_directory_path


class Profile(models.Model):
    """
    Define the Profile Model (linked to the User Model).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to=user_directory_path,
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.fullname


class Skill(models.Model):
    """
    Holds the list of pre-defined and custom skills.
    """
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, default='p')  # p (preset) or c (custom).

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """
    Link the user to one or many skills.
    """
    user = models.ForeignKey(User, related_name='user_skill', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='skill_user', on_delete=models.CASCADE)
    is_skill = models.BooleanField(default=False)


class Portfolio(models.Model):
    """
    Model to hold the user's portfolio links
    (labeled as 'My Projects' in the design).
    """
    user = models.ForeignKey(User, related_name='user_portfolio', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name








