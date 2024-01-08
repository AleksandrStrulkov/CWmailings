from django.db import connection
from django.contrib.auth import get_user_model
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    client_email = models.EmailField(unique=False, verbose_name='Email')
    first_name = models.CharField(max_length=255, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', **NULLABLE)
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    client_owner = models.ForeignKey(get_user_model(), verbose_name='Пользователь',
                                    on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.client_email} {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'ALTER SEQUENCE catalog_statusproduct_id_seq RESTART WITH 1;')


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема рассылки')
    content = models.TextField(verbose_name='Содержание рассылки')
    message_owner = models.ForeignKey(get_user_model(), verbose_name='Пользователь',
                                    on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'ALTER SEQUENCE catalog_statusproduct_id_seq RESTART WITH 1;')


class MailingOptions(models.Model):
    PERIOD_MAILING = (
            (None, 'Выберите периодичность рассылки'),
            ('Ежедневно', 'Ежедневно'),
            ('Еженедельно', 'Еженедельно'),
            ('Ежемесячно', 'Ежемесячно')
    )

    STATUS_MAILING = (
            ('Создана', 'Создана'),
            ('Запущена', 'Запущена'),
            ('Завершена', 'Завершена')
    )
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE, default=None)
    start_time = models.DateTimeField(verbose_name='Дата начала рассылки', default=None)
    finish_time = models.DateTimeField(verbose_name='Дата окончания рассылки', default=None)
    creation_date = models.DateTimeField(verbose_name='Дата и время создания', auto_now=True)
    send_period = models.CharField(max_length=20, verbose_name='Периодичность',
                                   choices=PERIOD_MAILING)
    send_status = models.CharField(max_length=20, verbose_name='Статус рассылки',
                                   choices=STATUS_MAILING, default='Создана')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    next_attempt = models.DateTimeField(verbose_name='Дата последней отправки', **NULLABLE)
    mailing_owner = models.ForeignKey(get_user_model(), verbose_name='Пользователь',
                            on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.message} ({self.start_time})"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['pk']

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'ALTER SEQUENCE catalog_statusproduct_id_seq RESTART WITH 1;')


class Logs(models.Model):
    last_attempt_time = models.DateTimeField(verbose_name='Последняя отправка рассылки',
                                             auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=20, verbose_name='Статус отправки рассылки')
    mailing = models.ForeignKey(MailingOptions, verbose_name='Рассылка', on_delete=models.CASCADE)
    error_message = models.TextField(verbose_name='Сообщение об ошибке', **NULLABLE)
    client = models.ForeignKey(get_user_model(), verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)
    send_email = models.EmailField(max_length=150, verbose_name='почта отправки', **NULLABLE)

    def __str__(self):
        return (f'{self.last_attempt_time} '
                f'{self.status} '
                f'{self.mailing} '
                f'{self.error_message}')

    class Meta:
        verbose_name = ('Лог')
        verbose_name_plural = ('Логи')
