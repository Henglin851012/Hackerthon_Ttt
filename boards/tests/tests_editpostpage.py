from django.test import TestCase
from django.urls import reverse
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User

class EditPostPage_Test(TestCase):

	"""
	1. url accessible, status code, url_name and function resolving - all correct args
	2. url accessible - correct board and topic but incorrect post id
	3. url accessible for incorrect topic but correct board
	4. url accessible for incorrect board
	5. correct links present
	6. correct data - post edited and redirection
	7. empty data - same page rendering
	8. incorrect data - same page rendering
	9. check if any other user can edit someone else's post
	"""

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='test1', email='test1@test.com', password='test123')
		cls.user2 = User.objects.create_user(username='test2', email='test2@test.com', password='test456')
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.topic = Topic.objects.create(subject='Test', board=cls.board, created_by=cls.user)
		cls.post = Post.objects.create(message='Test1', topic=cls.topic, created_by=cls.user)
		cls.homeurl = reverse('home_url')
		cls.boardtopics_url = reverse('board_topics_url', kwargs={'board_id':cls.board.id})
		cls.topicpageurl = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.editposturl_correct = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id, 'post_id':cls.post.id})
		cls.editposturl_wrongboard = reverse('post_edit_url', kwargs={'board_id':99, 'topic_id':cls.topic.id, 'post_id':cls.post.id})
		cls.editposturl_wrongtopic = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':99, 'post_id':cls.post.id})
		cls.editposturl_wrongpost = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id, 'post_id':99})
		cls.editpostpath_correct = '/board/{}/topic/{}/post/{}/edit/'.format(cls.board.id, cls.topic.id, cls.post.id)
		cls.cancelediturl = '{url}?page={pageno}#{postid}'.format(url=cls.topicpageurl, pageno=cls.topic.get_pageno_of_post(cls.post), postid=cls.post.id)

	def setUp(self):
		self.client.login(username='test1', password='test123')

	def test_1(self):
		response = self.client.get(self.editposturl_correct)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		response = self.client.get(self.editposturl_wrongpost)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.editposturl_wrongtopic)
		self.assertEqual(response.status_code, 404)

	def test_4(self):
		response = self.client.get(self.editposturl_wrongboard)
		self.assertEqual(response.status_code, 404)

	def test_5(self):
		response = self.client.get(self.editposturl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.boardtopics_url))
		self.assertContains(response, 'href="{}"'.format(self.topicpageurl))
		self.assertContains(response, 'href="{}"'.format(self.editposturl_correct))
		self.assertContains(response, 'href="{}"'.format(self.cancelediturl), 1)

	def test_6(self):
		response = self.client.post(self.editposturl_correct, data={'message': 'Edit message'}, follow=True)
		topicurl_pageid = '{url}?page={pageno}#{postid}'.format(url=self.topicpageurl, pageno=self.topic.get_pageno_of_post(self.post), postid=self.post.id)
		self.assertRedirects(response=response, expected_url=topicurl_pageid, status_code=302, target_status_code=200)

	def test_7(self):
		response = self.client.post(self.editposturl_correct, data={'message': ''})
		self.assertEqual(response.status_code, 200)

	def test_8(self):
		response = self.client.post(self.editposturl_correct, data={})
		self.assertEqual(response.status_code, 200)

	def test_9(self):
		self.client.login(username='test2', password='test456')
		response = self.client.get(self.editposturl_correct)
		self.assertEqual(response.status_code, 404)
