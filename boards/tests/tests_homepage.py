from django.test import TestCase
from django.urls import reverse
from boards.models import Board

# Create your tests here.

class HomePage_Test(TestCase):
	
	#1. check if home_url is giving correct status code 200
	#2. check if home page contains link to home page at breadcrumb navigation
	#3. check if home page contains link to topic in table

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.home_url = reverse('home_url')
		cls.boardtopics_url = reverse('board_topics_url', kwargs={'board_id':cls.board.id})

	def test_1(self):
		response = self.client.get(self.home_url)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		response = self.client.get(self.home_url)
		self.assertContains(response, 'href="{}"'.format(self.home_url))

	def test_3(self):
		response = self.client.get(self.home_url)
		self.assertContains(response, 'href="{}"'.format(self.boardtopics_url))
