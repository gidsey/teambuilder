# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.urls import reverse
# from accounts.factories import UserFactory
# from accounts.models import Profile
#
#
# class ProfileViewTest(TestCase):
#     def test_profile_edit(self):
#         user = UserFactory()
#         self.client.login(username=user.email, password='pass')
#         print(user)
#         response = self.client.post(reverse('accounts:user_profile', args={user}))
#         print(response)
#         # Get the user again
#         user = User.objects.get(id=user.id)
#         print(user)
#         print(user.email)
#         print(user.profile)
#         # profile = Profile.objects.get(user=user)
#
#         self.assertEqual(user.profile.fullname, 'Full Name')
#         self.assertEqual(user.bio, 'Considering first party data in order to think outside the box.')
#         # self.assertEqual(user_link.anchor, 'My Link')
#         # self.assertEqual(user_link.url, 'http://mylink.com/')
#
#
#
# # class ProfileSettingsTest(TestCase):
# #     def test_profile_edit(self):
# #         user = UserFactory()
# #         self.client.login(username=user.email, password='pass')
# #         print(user)
# #         response = self.client.post(
# #             reverse('accounts:user_profile_edit', args={user}),
# #             data={
# #                 'profile-fullname': 'Full Name',
# #                 'profile-bio': "Considering first party data in order to think outside the box.",
# #                 'profile-skills': [1, 10],
# #                 'form-TOTAL_FORMS': 1,
# #                 'form-INITIAL_FORMS': 0,
# #                 'folio-items-0-name': 'Test Website',
# #                 'folio-items-0-url': 'https://test.com',
# #                 'folio-items-1-name': 'Test Different Website',
# #                 'folio-items-1-url': 'https://new.com',
# #                 'CSForm-0-name': 'Tester',
# #                 'CSForm-1-name': 'Project Manager',
# #             },
# #         )
# #         print(response)
# #         # Get the user again
# #         user = User.objects.get(id=user.id)
# #         print(user)
# #         print(user.email)
# #         print(user.profile)
# #         # profile = Profile.objects.get(user=user)
# #
# #         self.assertEqual(user.profile.fullname, 'Full Name')
# #         self.assertEqual(user.bio, 'Considering first party data in order to think outside the box.')
# #         # self.assertEqual(user_link.anchor, 'My Link')
# #         # self.assertEqual(user_link.url, 'http://mylink.com/')
