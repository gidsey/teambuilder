# from django.test import RequestFactory, TestCase
# from projects import models
# from projects import views
#
#
# class ProjectViewsTests(TestCase):
#     """
#     Test the Project views
#     """
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_search_view(self):
#         """
#         Test Keyword Search across Project Title and Definition
#         'clean' used as search term
#         """
#         request = self.factory.get('projects/search/', {'q': 'cledan'})
#
#         response = views.project_search(request)
#         self.assertEqual(response.status_code, 200)
#         # self.assertContains(response, self.axinite.name)
#         # self.assertNotContains(response, self.barstowite.name)