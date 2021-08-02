from django import forms
from django.forms import BooleanField

from boards.models import Post
from mdeditor.fields import MDTextFormField

class TopicReply_Form(forms.ModelForm):
	message = MDTextFormField()
	anonymous = BooleanField(required=False)
	class Meta:
		model = Post
		fields = ['message', 'anonymous']
		
		
	