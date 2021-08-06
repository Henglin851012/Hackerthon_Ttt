from django.test import TestCase
from django.urls import reverse
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User

class NewTopicPage_Test(TestCase):

	"""
	1. check if new_topic_url is giving correct status code 200 (correct board id)
	2. check if new_topic_url is giving correct status code 404 (incorrect board id)
	3. check if new topic page contains correct links at breadcrumb navigation
	4. check if new topic/post created for valid data, logged in user is creater of topic/post, topic of post is currently created topic and redirects successful
	5. check if new topic/post not created for invalid data and no redirects
	6. check if new topic/post not created for empty  data and no redirects
	"""

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.newtopicurl_correct = reverse('new_topic_url', kwargs={'board_id':cls.board.id})
		cls.newtopicurl_incorrect = reverse('new_topic_url', kwargs={'board_id': 99})
		cls.pathcorrect = '/board/' + str(cls.board.id) + '/newtopic/'
		cls.homeurl = reverse('home_url')
		cls.boardtopicpageurl = reverse('board_topics_url', kwargs={'board_id': cls.board.id})

	def setUp(self):
		self.client.login(username='Test', password='test123')

	def test_1(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		response = self.client.get(self.newtopicurl_incorrect)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.boardtopicpageurl))
		self.assertContains(response, 'href="{}"'.format(self.newtopicurl_correct))

	def test_4(self):
		response = self.client.post(self.newtopicurl_correct,follow=True, data={'subject':'Test', 'message':'Test'})
		self.assertTrue(Topic.objects.exists())
		self.assertTrue(Post.objects.exists())
		self.assertEqual(Topic.objects.get(subject='Test').created_by, response.context.get('user'))
		self.assertEqual(Post.objects.get(message='Test').created_by, response.context.get('user'))
		self.assertEqual(Topic.objects.get(subject='Test'), Post.objects.get(message='Test').topic)
		topic = Topic.objects.first()
		topicpageurl = reverse('topic_page_url', kwargs={'board_id':self.board.id, 'topic_id':topic.id})
		self.assertRedirects(response=response, expected_url=topicpageurl, status_code=302, target_status_code=200)

	def test_5(self):
		response = self.client.post(self.newtopicurl_correct, data={})
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())
		self.assertEqual(response.status_code, 200)

	def test_6(self):
		response = self.client.post(self.newtopicurl_correct, data={'subject': '', 'message':''})
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())
		self.assertEqual(response.status_code, 200)
