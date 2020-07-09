from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestEditProfile(TestCase):

    def test_edit_profile(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )
        login = self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
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
        self.assertEqual(user.profile.fullname, 'Test User')
        self.assertEqual(user.profile.bio, 'Build key demographics and try to be transparent.')
