import slugify as slugify
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from CWmailings import settings
from blog.forms import BlogForm
from blog.models import Blog
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


class BlogCreateView(CreateView):
	model = Blog
	# permission_required = 'blog.add_blog'
	form_class = BlogForm
	success_url = reverse_lazy('blog:list')
	extra_context = {
			'title': "Добавить публикацию",
	}

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('users:register')
		else:
			return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		if form.is_valid():
			new_mat = form.save()
			new_mat.slug = slugify(new_mat.title)
			new_mat.save()

		return super().form_valid(form)


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
	model = Blog
	permission_required = 'blog.change_blog'
	form_class = BlogForm
	success_url = reverse_lazy('blog:list')
	extra_context = {
			'title': "Редактировать публикацию",
	}

	def form_valid(self, form):
		if form.is_valid():
			new_mat = form.save()
			new_mat.slug = slugify(new_mat.title)
			new_mat.save()

		return super().form_valid(form)

	def get_success_url(self):
		return reverse('blog:view', args=[self.kwargs.get('slug')])


# class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
class BlogDeleteView(PermissionRequiredMixin, DeleteView):
	model = Blog
	success_url = reverse_lazy('blog:list')
	permission_required = 'blog.delete_blog'
	extra_context = {
			'title': "Удаление публикации",
	}

	def test_func(self):
		return self.request.user.is_superuser


class BlogListView(ListView):
	model = Blog
	extra_context = {
			'title': "Все публикации",
	}

	def get_queryset(self, *args, **kwargs):
		queryset = super().get_queryset(*args, **kwargs)
		queryset = queryset.filter(is_published=True)
		return queryset


class BlogDetailView(DetailView):
	model = Blog
	extra_context = {
			'title': "Приятного прочтения",
	}

	def get_object(self, queryset=None):
		self.object = super().get_object(queryset)
		self.object.views_count += 1
		self.object.save()
		return self.object


# def toggle_activity(request, slug):
# 	blog_item = get_object_or_404(Blog, slug=slug)
# 	if blog_item.is_published:
# 		blog_item.is_published = False
# 	else:
# 		blog_item.is_published = True
#
# 	blog_item.save()
#
# 	return redirect(reverse('blog:list'))
