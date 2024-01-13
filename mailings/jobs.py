import smtplib
from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from mailings.models import MailingOptions, Logs


def my_job():
	minutes: timedelta = timedelta(days=0, hours=0, minutes=1)
	day: timedelta = timedelta(days=1, hours=0, minutes=0)
	weak: timedelta = timedelta(days=7, hours=0, minutes=0)
	month: timedelta = timedelta(days=30, hours=0, minutes=0)
	now = datetime.now()
	now = datetime.now(pytz.timezone('Europe/Moscow'))

	mailings = MailingOptions.objects.all().filter(send_status='Создана') \
		.filter(is_active=True) \
		.filter(next_attempt__lte=now) \
		.filter(finish_time__gte=now)

	for mailing in mailings:
		mailing.send_status = 'Запущена'
		mailing.save()
		emails_list = [client.client_email for client in mailing.clients.all()]
		print(mailing.start_time)

		try:
			result = send_mail(
					subject=mailing.message.title,
					message=mailing.message.content,
					from_email=settings.EMAIL_HOST_USER,
					recipient_list=emails_list,
					fail_silently=False,
			)

			status = 'Oтправлено'
			error_message = ''

		except smtplib.SMTPException as e:
			status = 'Ошибка отправки'
			if 'authentication filed' in str(e):
				error_message = 'Ошибка на почтовом сервисе'
			elif 'suspicion of SPAM' in str(e):
				error_message = 'Определено как спам'
			else:
				error_message = e
		finally:
			log = Logs(
					last_attempt_time=now,
					status=status,
					mailing=mailing,
					error_message=error_message,
					client=mailing.mailing_owner,
					send_email=settings.EMAIL_HOST_USER
			)
			log.save()

			if mailing.send_period == 'Ежедневно':
				mailing.next_attempt = now + day
			elif mailing.send_period == 'Еженедельно':
				mailing.next_attempt = now + weak
			elif mailing.send_period == 'Ежемесячно':
				mailing.next_attempt = now + month
			elif mailing.send_period == 'Ежеминутно':
				mailing.next_attempt = now + minutes

			if mailing.next_attempt < mailing.finish_time:
				mailing.send_status = 'Создана'
			else:
				mailing.send_status = 'Завершена'
			mailing.save()