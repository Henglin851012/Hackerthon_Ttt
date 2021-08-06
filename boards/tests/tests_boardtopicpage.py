from django.test import TestCase
from django.urls import reverse
from boards.models import Board,Topic

class BoardTopicPage_Test(TestCase):

	#1. check if board_topics_url is giving correct status code 200 (correct board id)
	#2. check if board_topics_url is giving correct status code 404 (incorrect board id)
	#3. check if links are present

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.homeurl = reverse('home_url')
		cls.topicurl_correct = reverse('board_topics_url', kwargs={'board_id': cls.board.id})
		cls.topicurl_incorrect = reverse('board_topics_url', kwargs={'board_id':99})
		cls.newtopicurl_correct = reverse('new_topic_url', kwargs={'board_id': cls.board.id})
		cls.topic = Topic.objects.create(subject='Test',board=cls.board)
		cls.topicpageurl = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		
	def test_1(self):
		response = self.client.get(self.topicurl_correct)
		self.assertEqual(response.status_code, 200)

	def test2(self):
		response = self.client.get(self.topicurl_incorrect)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.topicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.topicurl_correct))
		self.assertContains(response, self.newtopicurl_correct)
		self.assertContains(response, self.topicpageurl)

