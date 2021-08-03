from django import forms
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from boards.models import Post
from mdeditor.fields import MDTextFormField

class TopicReply_Form(forms.ModelForm):
	message = MDTextFormField()
	class Meta:
		model = Post
		fields = ['message', 'anonymous']
		widgets = {'subject': forms.TextInput(attrs={'placeholder': 'enter subject of topic here'}),
				   'anonymous': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-primary")}
		
		
	