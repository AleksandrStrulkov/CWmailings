from mailings.apps import MailingsConfig
from django.urls import path

from mailings.views import MailingTemplateView, MessageUpdateView, MessageDeleteView, ClientListView, \
	ClientUpdateView, ClientCreateView, ClientDeleteView, ClientDetailView, MessageListView, MessageCreateView, \
	MessageDetailView, MailingOptionsCreateView, MailingOptionsDetailView, MailingOptionsListView, \
	MailingOptionsDeleteView

app_name = MailingsConfig.name


urlpatterns = [
		path('', MailingTemplateView.as_view(), name='home'),
		path('all_message/', MessageListView.as_view(), name='message_list'),
		path('message/detail', MessageDetailView.as_view(), name='message_detail'),
		path('message/create', MessageCreateView.as_view(), name='message_create'),
		path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
		path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

		path('client/', ClientListView.as_view(), name='client_list'),
		path('client/create', ClientCreateView.as_view(), name='client_create'),
		path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
		path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
		path('client/detail', ClientDetailView.as_view(), name='client_detail'),

		path('options/create', MailingOptionsCreateView.as_view(), name='options_create'),
		path('options/detail', MailingOptionsDetailView.as_view(), name='options_detail'),
		path('options/', MailingOptionsListView.as_view(), name='options_list'),
		path('options/delete/<int:pk>', MailingOptionsDeleteView.as_view(), name='options_delete'),
]
