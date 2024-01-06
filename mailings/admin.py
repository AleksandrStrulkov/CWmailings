from django.contrib import admin
from mailings.models import Client, Message, MailingOptions, Logs


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('client_email', 'first_name', 'last_name', 'comment')
	list_filter = ('client_email',)
	search_fields = ('first_name', 'last_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'content')


@admin.register(MailingOptions)
class MailingOptionsAdmin(admin.ModelAdmin):
	list_display = ('id', 'message', 'start_time', 'finish_time', 'creation_date', 'send_period', 'send_status',
				'is_active', 'next_attempt')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
	list_display = ('id', 'last_attempt_time', 'status', 'mailing', 'error_message', 'client')
