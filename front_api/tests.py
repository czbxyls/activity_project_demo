from django.test import TestCase
from activitylib import models

# Create your tests here.
class FrontTestCase(TestCase):
	def setUp(self):
		models.User.objects.create(username="test", password="roar", user_id=1, email='test',photo_url='test',create_time=1,update_time=1)
		pass

	def test_db(self):
		print models.User.objects.all()
