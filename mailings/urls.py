from mailings.apps import MailingsConfig
from django.urls import path

from mailings.views import MailingTemplateView, MailingListView, MailingCreateView, MessageUpdateView, \
	MessageDeleteView, MailingDetailView, ClientListView, ClientUpdateView, ClientCreateView, ClientDeleteView, \
	ClientDetailView

app_name = MailingsConfig.name


urlpatterns = [
		path('', MailingTemplateView.as_view(), name='home'),
		path('all_message/', MailingListView.as_view(), name='message_list'),
		path('message/detail', MailingDetailView.as_view(), name='message_detail'),
		path('message/create', MailingCreateView.as_view(), name='message_create'),
		path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
		path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
		path('client/<int:pk>', ClientListView.as_view(), name='client_list'),
		path('client/create', ClientCreateView.as_view(), name='client_create'),
		path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
		path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
		path('client/detail', ClientDetailView.as_view(), name='client_detail'),
]
