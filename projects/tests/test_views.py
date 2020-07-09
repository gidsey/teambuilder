from django.test import TestCase

from projects import models
from projects import views


class ProjectViewsTests(TestCase):
    """
    Test the Project views
    """

    def test_edit_profile(self):
        user = demo.factories.UserFactory.create()
        self.client.login(username=user.username, password='abc')