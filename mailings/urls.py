from mailings.apps import MailingsConfig
from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from mailings.views import MailingTemplateView, MessageUpdateView, MessageDeleteView, ClientListView, \
	ClientUpdateView, ClientCreateView, ClientDeleteView, ClientDetailView, MessageListView, MessageCreateView, \
	MailingOptionsCreateView, MailingOptionsListView, \
	MailingOptionsDeleteView, MailingOptionsUpdateView, LogsListView, UsersListView, UserOptionsUpdateView

app_name = MailingsConfig.name

urlpatterns = [
		path('', (MailingTemplateView.as_view()), name='home'),
		path('all_message/', cache_page(30)(MessageListView.as_view()), name='message_list'),
		path('message/create', MessageCreateView.as_view(), name='message_create'),
		path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
		path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

		path('client/', cache_page(30)(ClientListView.as_view()), name='client_list'),
		path('client/create', ClientCreateView.as_view(), name='client_create'),
		path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
		path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
		path('client/detail', ClientDetailView.as_view(), name='client_detail'),

		path('options/create', MailingOptionsCreateView.as_view(), name='options_create'),
		path('options/', cache_page(30)(MailingOptionsListView.as_view()), name='options_list'),
		path('options/delete/<int:pk>', MailingOptionsDeleteView.as_view(), name='options_delete'),
		path('options/update/<int:pk>', MailingOptionsUpdateView.as_view(), name='options_update'),

		path('options/logs/', LogsListView.as_view(), name='options_logs'),
		path('user_list/', UsersListView.as_view(), name='user_list'),
		path('user/update/<int:pk>', UserOptionsUpdateView.as_view(), name='user_update'),
]