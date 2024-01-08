from django.urls import path
from django.views.decorators.cache import never_cache, cache_page

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name


urlpatterns = [
		path('create/', BlogCreateView.as_view(), name='create'),  # создание
		path('', (BlogListView.as_view()), name='list'),
		path('view/<slug:slug>', cache_page(60)(BlogDetailView.as_view()), name='view'),
		path('edit/<slug:slug>', BlogUpdateView.as_view(), name='edit'),
		path('delete/<slug:slug>', BlogDeleteView.as_view(), name='delete'),
		# path('activity/<slug:slug>', toggle_activity, name='toggle_activity'),
]