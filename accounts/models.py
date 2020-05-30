from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    """Get the user directory path"""
    # file will be uploaded to MEDIA_ROOT/avatars/user/<filename>
    return 'avatars/{0}/{1}'.format(instance.user, filename)


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
        default='placeholder/default.jpg',
    )

    def __str__(self):
        return self.fullname


class Skill(models.Model):
    """
    Hold the list of pre-defined and custom skills.
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









