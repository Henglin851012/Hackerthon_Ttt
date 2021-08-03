from django import forms
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from boards.models import Topic
from mdeditor.fields import MDTextFormField

class NewTopic_Form(forms.ModelForm):
	message = MDTextFormField()
	class Meta:
		model = Topic
		fields = ['subject', 'message', 'anonymous']
		help_texts = {'subject':'Maximum length is 300'}
		widgets = {'subject':forms.TextInput(attrs={'placeholder': 'enter subject of topic here'}),
				   'anonymous':DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-primary")}	#model field subject is CharField so produces form field Charfield which has widget as TextInput
		#subject is of Topic and message(for Post ) declared outside Meta
