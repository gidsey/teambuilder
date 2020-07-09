from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project


class TestProjects(TestCase):

    def test_create_new_project(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )

        self.client.login(username='testuser', password='testpassword')

        self.client.post(
            reverse('projects:project_new'),
            data={
                'project-title': 'New Project',
                'project-description': 'This is a new project',
                'timeline': '1 Month',
                'requirements': 'Remote working',
                'position-items-TOTAL_FORMS': 1,
                'position-items-INITIAL_FORMS': 0,
                'position-items-0-title': 'Head of Testing',
                'position-items-0-description': 'With an electronic image sensor',
            },
        )

        user = User.objects.get(id=self.user.id)
        user_project = Project.objects.get(owner_id=user.id)
        self.assertEqual(user.owner_project.get(owner_id=self.user.id), user_project)

    def test_edit_project(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )

        self.project = Project.objects.create(
            owner_id=self.user.id,
            title='New Project',
            description='This is a new project',
            timeline='1 Month',
            requirements='Remote working'
        )

        self.client.login(username='testuser', password='testpassword')

        self.client.post(
            reverse('projects:project_edit', args={self.project.id}),
            data={
                'project-title': 'Newer Project',
                'project-description': 'This is a a change to the new project',
                'timeline': '1.5 Months',
                'requirements': 'Remote working only',
                'position-items-TOTAL_FORMS': 1,
                'position-items-INITIAL_FORMS': 0,
                'position-items-0-title': 'Head of Testing',
                'position-items-0-description': 'Without an electronic image sensor',
                'project-skills': [1, 10],
            },
        )

        user = User.objects.get(id=self.user.id)
        user_project = Project.objects.get(owner_id=user.id)

        self.assertEqual(user_project.title, 'Newer Project')
        self.assertEqual(user_project.description, 'This is a a change to the new project')


