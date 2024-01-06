import logging
import pytz
from datetime import datetime, timedelta
import calendar
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.db.models import QuerySet
from mailings.models import MailingOptions
from mailings.services import send_mail_and_log

logger = logging.getLogger(__name__)

# mailing_list = MailingOptions.objects.all()


# def job():
current_time = datetime.now().replace(tzinfo=pytz.UTC)
current_time_str: str = datetime.now().strftime('%Y-%m-%d %H:%M')
# mailings: QuerySet = MailingOptions.objects.filter(send_status='Создана')
mailings = MailingOptions.objects.all()


def my_job_sec():
	for mailing in mailings:
		if mailing.is_active:
			if mailing.send_status == 'Создана':
				if mailing.start_time <= current_time_str:
					mailing.start_time = current_time_str
					mailing.send_status = 'Запущена'
					mailing.save()
			if mailing.send_status == 'Запущена':
				if mailing.finish_time <= current_time_str:
					mailing.send_status = 'Завершена'
					mailing.save()
				elif mailing.start_time <= current_time_str:
					send_mail_and_log(mailing)
					if mailing.send_period == 'Ежедневно':
						mailing.next_attempt = current_time + timedelta(days=1)
					elif mailing.send_period == 'Еженедельно':
						mailing.next_attempt = current_time + timedelta(days=7)
					elif mailing.send_period == 'Ежемесячно':
						today = datetime.today()
						days = calendar.monthrange(today.year, today.month)[1]
						mailing.next_attempt = current_time + timedelta(days=days)

					mailing.save()


def my_job_daily():
	for mailing in mailings:
		if mailing.is_active:
			if mailing.send_status == 'Создана':
				if mailing.start_time <= current_time_str:
					mailing.start_time = current_time_str
					mailing.send_status = 'Запущена'
					mailing.save()
			if mailing.send_status == 'Запущена':
				if mailing.finish_time <= current_time_str:
					mailing.send_status = 'Завершена'
					mailing.save()
				elif mailing.start_time <= current_time_str:
					send_mail_and_log(mailing)
					if mailing.send_period == 'Ежедневно':
						mailing.next_attempt = current_time + timedelta(days=1)
					elif mailing.send_period == 'Еженедельно':
						mailing.next_attempt = current_time + timedelta(days=7)
					elif mailing.send_period == 'Ежемесячно':
						today = datetime.today()
						days = calendar.monthrange(today.year, today.month)[1]
						mailing.next_attempt = current_time + timedelta(days=days)

					mailing.save()


def my_job_weekly():
	for mailing in mailings:
		if mailing.is_active:
			if mailing.send_status == 'Создана':
				if mailing.start_time <= current_time_str:
					mailing.start_time = current_time_str
					mailing.send_status = 'Запущена'
					mailing.save()
			if mailing.send_status == 'Запущена':
				if mailing.finish_time <= current_time_str:
					mailing.send_status = 'Завершена'
					mailing.save()
				elif mailing.start_time <= current_time_str:
					send_mail_and_log(mailing)
					if mailing.send_period == 'Ежедневно':
						mailing.next_attempt = current_time + timedelta(days=1)
					elif mailing.send_period == 'Еженедельно':
						mailing.next_attempt = current_time + timedelta(days=7)
					elif mailing.send_period == 'Ежемесячно':
						today = datetime.today()
						days = calendar.monthrange(today.year, today.month)[1]
						mailing.next_attempt = current_time + timedelta(days=days)

					mailing.save()


def my_job_monthly():
	for mailing in mailings:
		if mailing.is_active:
			if mailing.send_status == 'Создана':
				if mailing.start_time <= current_time_str:
					mailing.start_time = current_time_str
					mailing.send_status = 'Запущена'
					mailing.save()
			if mailing.send_status == 'Запущена':
				if mailing.finish_time <= current_time_str:
					mailing.send_status = 'Завершена'
					mailing.save()
				elif mailing.start_time <= current_time_str:
					send_mail_and_log(mailing)
					if mailing.send_period == 'Ежедневно':
						mailing.next_attempt = current_time + timedelta(days=1)
					elif mailing.send_period == 'Еженедельно':
						mailing.next_attempt = current_time + timedelta(days=7)
					elif mailing.send_period == 'Ежемесячно':
						today = datetime.today()
						days = calendar.monthrange(today.year, today.month)[1]
						mailing.next_attempt = current_time + timedelta(days=days)

					mailing.save()


# Декоратор close_old_connections гарантирует, что соединения с базой данных, которые стали
# непригодны для использования или устарели, закрываются до и после выполнения вашего задания. Вы должны #использовать это
# для обертывания любых запланированных вами заданий, которые каким-либо образом обращаются к базе данных Django.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
	"""
	Это задание удаляет из базы данных записи выполнения заданий APScheduler старше max_age.
	Это помогает предотвратить заполнение базы данных старыми историческими записями, которые не являются
	дольше полезно.
	:param max_age: Максимальный срок хранения исторических записей выполнения заданий.
					По умолчанию 7 дней.
	"""
	DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
	help = "Runs APScheduler."

	def handle(self, *args, **options):
		scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(), "default")

		scheduler.add_job(
				my_job_sec,
				trigger=CronTrigger(second="*/10"),  # Каждые 10 секунд
				id="my_job_sec",  # Идентификатор, присвоенный каждому заданию, ДОЛЖЕН быть уникальным.
				max_instances=1,
				replace_existing=True,
		)
		logger.info("Добавлена каждые 10 секунд 'my_job'.")

		scheduler.add_job(
				my_job_daily,
				trigger=CronTrigger(hour="*/23"),  # Каждые 23 часа.
				id="my_job_daily",
				max_instances=1,
				replace_existing=True,
		)
		logger.info(
				"Добавлено ежедневное задание: 'delete_old_job_executions'."
		)

		scheduler.add_job(
				my_job_weekly,
				trigger=CronTrigger(
						day_of_week="sat", hour="12", minute="00"
				),  # Полночь понедельника, перед началом следующей рабочей недели.
				id="my_job_weekly",
				max_instances=1,
				replace_existing=True,
		)
		logger.info(
				"Добавлено еженедельное задание: 'delete_old_job_executions'.")

		scheduler.add_job(
				my_job_monthly,
				trigger=CronTrigger(
						day="6", hour="12", minute="00"
				),  # Первый день месяца
				id="delete_old_job_executions",
				max_instances=1,
				replace_existing=True,
		)
		logger.info(
				"Добавлено ежемесячное задание: 'delete_old_job_executions'."
		)

		scheduler.add_job(
				delete_old_job_executions,
				trigger=CronTrigger(
						day_of_week="mon", hour="00", minute="00"
				),  # Midnight on Monday, before start of the next work week.
				id="delete_old_job_executions",
				max_instances=1,
				replace_existing=True,
		)
		logger.info(
				"Added weekly job: 'delete_old_job_executions'."
		)

		try:
			logger.info("Starting scheduler...")
			scheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping scheduler...")
			scheduler.shutdown()
			logger.info("Scheduler shut down successfully!")