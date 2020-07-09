from django.contrib.auth.models import User
import factory
from accounts import models


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = 'john'
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)



class UserProfile(factory.Factory):
    class Meta:
        model = models.Profile



