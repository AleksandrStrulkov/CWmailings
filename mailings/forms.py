from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from mailings.models import Client, Message, MailingOptions


class StyleFormMixin:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if field_name in ['send_period', 'send_status', 'clients']:
				field.widget.attrs['class'] = 'form-select'
			elif field_name == 'is_active':
				field.widget.attrs['class'] = 'form'
			else:
				field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = MailingOptions
		exclude = ('mailing_owner', 'send_status',)


class ClientForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = Client
		exclude = ('client_owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = Message
		exclude = ('message_owner',)


class MailingManagerForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = MailingOptions
		fields = ('is_active',)


class MailingOptionsForm(StyleFormMixin, forms.ModelForm):
	class Meta:
		model = MailingOptions
		exclude = ('next_try', 'options_owner', 'send_status',)