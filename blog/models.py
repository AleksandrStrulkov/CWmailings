from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
	title = models.CharField(max_length=50, verbose_name='Заголовок')
	body = models.TextField(verbose_name='Содержимое')
	image = models.ImageField(upload_to='images_blog/', verbose_name='Изображение', **NULLABLE)
	updated_at = models.DateField(auto_now=True, verbose_name='Дата публикации')
	is_published = models.BooleanField(verbose_name='Опубликовано', default=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'блог'
		verbose_name_plural = 'Блоги'


# Create your models here.
