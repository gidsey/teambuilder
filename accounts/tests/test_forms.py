from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

from accounts import forms

client = Client()


class TestProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpassword',
        )
        login = self.client.login(username='testuser', password='testpassword', )

    def test_edit_profile(self):
        """
        Test logged-in access to the edit profile page.
        """
        username = self.user
        response = self.client.get(reverse('accounts:user_profile_edit', args={username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

    def test_profile_form(self):
        """
        Test the profile form.
        """
        form_data = {
            'profile-fullname': 'Test User',
            'profile-bio': "Considering first party data in order to think outside the box.",
            'profile-skills': [1, 10]
        }
        form = forms.ProfileForm(
            prefix='profile',
            instance=self.user,
            data=form_data,
            choices=[(1, 'Android Developer'), (2, 'Designer'), (10, 'Django Developer')]
        )
        self.assertTrue(form.is_valid())

    def test_portfolio_inline_formset(self):
        """
        Test the portfolio inline formset on the profile edit/create page.
        """
        form_data = {
            'folio-items-name': 'Test Website',
            'folio-items-url': 'https://test.com',
            'folio-items-TOTAL_FORMS': 1,
            'folio-items-INITIAL_FORMS': 0,
        }
        form = forms.portfolio_inline_formset(
            data=form_data,
            instance=self.user,
            prefix='folio-items',
        )
        self.assertTrue(form.is_valid())

    def test_custom_skills_formset(self):
        """
        Test the custom skills formset on the profile edit/create page.
        """
        form_data = {
            'CSForm-name': 'Tester',
            'CSForm-TOTAL_FORMS': 1,
            'CSForm-INITIAL_FORMS': 0,
        }
        form = forms.CustomSkillsFormSet(
            data=form_data,
            prefix='CSForm',
        )
        self.assertTrue(form.is_valid())