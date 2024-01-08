
# Register your models here.
from django.contrib import admin
from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'body', 'image', 'updated_at', 'is_published', 'views_count',)
    list_filter = ('title',)
    search_fields = ('title', 'body',)


