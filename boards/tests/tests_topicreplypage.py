from django.test import TestCase
from django.urls import reverse
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User

class TopicReplyPage_Test(TestCase):

	"""
	1. url status code, url name , func resolving for correct board id and topic id
	2. url for incorrect topic id but correct board id
	3. url for incorrect board id
	4. link to home page, board topicpage, topic page and reply page
	5. correct data - post created - redirection
	6. incorrect data - same page - post not created
	7. empty data - same page - post not created
	"""

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.topic = Topic.objects.create(subject='Test', board=cls.board, created_by=cls.user)
		cls.replytopicurl_correct = reverse('topic_reply_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.replytopicpath_correct = '/board/{}/topic/{}/reply/'.format(cls.board.id, cls.topic.id)
		cls.replytopicurl_wrongboard = reverse('topic_reply_url', kwargs={'board_id':99, 'topic_id':cls.topic.id})
		cls.replytopicurl_wrongtopic = reverse('topic_reply_url', kwargs={'board_id':cls.board.id, 'topic_id':99})
		cls.homeurl = reverse('home_url')
		cls.boardtopicsurl = reverse('board_topics_url', kwargs={'board_id':cls.board.id})
		cls.topicurl = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.formfields_seq = ['message', 'anonymous']
		cls.replytopicdata_correct = {'message': 'Test message'}

	#login needed
	def setUp(self):
		self.client.login(username='Test', password='test123')

	def test_1(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		response = self.client.get(self.replytopicurl_wrongtopic)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.replytopicurl_wrongboard)
		self.assertEqual(response.status_code, 404)

	def test_4(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.boardtopicsurl))
		self.assertContains(response, 'href="{}"'.format(self.topicurl))
		self.assertContains(response, 'href="{}"'.format(self.replytopicurl_correct))

	def test_5(self):
		response = self.client.post(self.replytopicurl_correct, data=self.replytopicdata_correct, follow=True)
		self.assertTrue(Post.objects.exists())
		post = Post.objects.first()
		self.topicurl_with_page_id = '{url}?page={pageno}#{postid}'.format(url=self.topicurl, pageno=self.topic.get_last_posts_pageno(), postid=post.id)
		self.assertRedirects(response=response, expected_url=self.topicurl_with_page_id, status_code=302, target_status_code=200)	#redirected to topic page

	def test_6(self):
		response = self.client.post(self.replytopicurl_correct, data={})
		self.assertFalse(Post.objects.exists())
		self.assertEqual(response.status_code, 200)

	def test_7(self):
		response = self.client.post(self.replytopicurl_correct, data={'message': ''})
		self.assertFalse(Post.objects.exists())
		self.assertEqual(response.status_code, 200)
