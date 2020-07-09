from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project, Position, UserApplication
from accounts import models


class TestProjects(TestCase):

    def test_create_new_project(self):
        """
        Ensure a logged in user can create a new project
        """
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
        """
        Ensure a logged in user can edit a project.
        """
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

    def test_project_listing(self):
        """
        Test the project listing (home) page.
        """
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

        response = self.client.get(reverse('projects:project_listing', args={'all'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_listing.html')

    def test_project_detail(self):
        """
        Test the project detail page.
        """
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

        response = self.client.get(reverse('projects:project_detail', args={self.project.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_detail.html')

    def test_project_detail_apply(self):
        """
        Test the project detail page.
        """
        #  Create a user who owns the project
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )

        #  Create a different user who will apply for a position on the project
        self.applicant = User.objects.create_user(
            username='testapplicant',
            email='test.applicant@test.com',
            password='testpassword',
        )

        #  Assign a profile to the applicant
        self.applicant.profile = models.Profile.objects.create(
            user=self.applicant,
            fullname='Andy Applicant',
            bio='Siphon half and half seasonal coffee.'
        )

        self.project = Project.objects.create(
            owner_id=self.user.id,
            title='New Project',
            description='This is a new project',
            timeline='1 Month',
            requirements='Remote working'
        )

        self.position = Position.objects.create(
            project_id=self.project.id,
            title='Django developer',
            description='Everything hopped up on goofballs',
            filled=False,
        )

        self.client.login(username='testapplicant', password='testpassword')

        self.client.post(
            reverse('projects:project_detail', args={self.project.id}),
            data={
                'application': 'Apply',
                'position': self.position.id,
            },
        )
        applicant = User.objects.get(id=self.applicant.id)
        user_applications = UserApplication.objects.filter(user_id=self.applicant.id)
        self.assertQuerysetEqual(applicant.application_user.all(), user_applications, transform=lambda x: x)


class TestApplications(TestCase):

    def setUp(self):
        #  Create a user who owns the project
        self.user = User.objects.create_user(
            username='testuser',
            email='test.user@test.com',
            password='testpassword',
        )

        #  Assign a profile to the project owner
        self.user.profile = models.Profile.objects.create(
            user=self.user,
            fullname='Project Owner',
            bio='Half and half seasonal coffee.'
        )

        #  Create a different user who will apply for a position on the project
        self.applicant = User.objects.create_user(
            username='testapplicant',
            email='test.applicant@test.com',
            password='testpassword',
        )

        #  Assign a profile to the applicant
        self.applicant.profile = models.Profile.objects.create(
            user=self.applicant,
            fullname='Andy Applicant',
            bio='Siphon half and half seasonal coffee.'
        )

        self.project = Project.objects.create(
            owner_id=self.user.id,
            title='New Project',
            description='This is a new project',
            timeline='1 Month',
            requirements='Remote working'
        )

        self.position = Position.objects.create(
            project_id=self.project.id,
            title='Django developer',
            description='Everything hopped up on goofballs',
            filled=False,
        )

        self.application = UserApplication.objects.create(
            user_id=self.applicant.id,
            position_id=self.position.id,
            status=1,
        )

    def test_application_page(self):
        """
        Test the application listing page.
        """
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('projects:applications', args={self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/applications.html')

    def test_application_page_reject(self):
        """
        Test the application rejection mechanism.
        """
        self.client.login(username='testuser', password='testpassword')
        self.client.post(
            reverse('projects:applications', args={self.user.username}),
            data={
                'applicant': self.applicant.id,
                'reject': 'Reject',
                'position': self.position.id,
            },
        )
        applicant = User.objects.get(id=self.applicant.id)
        user_applications = UserApplication.objects.filter(user_id=self.applicant.id)
        self.assertQuerysetEqual(applicant.application_user.all(), user_applications, transform=lambda x: x)
