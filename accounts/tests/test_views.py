from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts import models
from projects.models import Project


class TestEditProfile(TestCase):

    def test_edit_or_create_profile(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )
        self.client.login(username='testuser', password='testpassword')

        self.client.post(
            reverse('accounts:user_profile_edit', args={self.user}),
            data={
                'profile-fullname': 'Test User',
                'profile-bio': "Build key demographics and try to be transparent.",
                'folio-items-TOTAL_FORMS': 1,
                'folio-items-INITIAL_FORMS': 0,
                'folio-items-0-name': 'Test Website',
                'folio-items-0-url': 'https://test.com',
                'CSForm-TOTAL_FORMS': 1,
                'CSForm-INITIAL_FORMS': 0,
                'CSForm-0-name': 'Tester',
            },
        )

        user = User.objects.get(id=self.user.id)
        user_portfolio = models.Portfolio.objects.filter(user_id=user.id)
        user_skills = models.UserSkill.objects.filter(user=user)

        self.assertEqual(user.profile.fullname, 'Test User')
        self.assertEqual(user.profile.bio, 'Build key demographics and try to be transparent.')
        self.assertQuerysetEqual(user.user_portfolio.all(), user_portfolio, transform=lambda x: x)
        self.assertQuerysetEqual(user.user_skill.all(), user_skills, transform=lambda x: x)

    def test_view_profile(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )

        self.user.profile = models.Profile.objects.create(
            user=self.user,
            fullname='Terry Tester',
            bio='Siphon half and half seasonal coffee.'
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
            reverse('accounts:user_profile', args={self.user}))

        user = User.objects.get(id=self.user.id)
        user_project = Project.objects.filter(owner_id=self.user.id)

        self.assertEqual(user.profile.fullname, 'Terry Tester')
        self.assertEqual(user.profile.bio, 'Siphon half and half seasonal coffee.')
        self.assertQuerysetEqual(user.owner_project.all(), user_project, transform=lambda x: x)

    def test_restricted_access_to_profile_edit(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2.user2@test.com',
            password='testpassword',
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:user_profile_edit', args={self.user2}))
        self.assertEqual(response.status_code, 403)

