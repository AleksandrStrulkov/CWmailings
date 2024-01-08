from django.urls import reverse_lazy

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from blog.models import Blog
from mailings.forms import MessageForm, ClientForm, MailingForm, MailingManagerForm, MailingOptionsForm
from mailings.models import MailingOptions, Client, Message, Logs
import random
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, \
    PermissionRequiredMixin


# class MailingTemplateView(TemplateView):


class MailingTemplateView(TemplateView):
    template_name = 'mailings/home.html'
    extra_context = {
            'title': "Главная страница",
    }

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        if self.request.method == 'GET':
            if settings.CASH_ENABLE:
                key = f'cached_statistics'
                cached_context = cache.get(key)
                if cached_context is None:
                    context = super().get_context_data(**kwargs)
                    context['all_mailings'] = MailingOptions.objects.all().count()
                    context['active_mailings'] = MailingOptions.objects.all().filter(is_active=True).count()
                    context['unique_clients_list'] = Client.objects.all().distinct('client_email').count()
                    main_page_context = {
                            'all_mailings': context['all_mailings'],
                            'active_mailings': context['active_mailings'],
                            'unique_clients_list': context['unique_clients_list']}
                    cache.set(key, main_page_context)
                    all_blog = Blog.objects.all()
                    random_blog = random.sample(list(all_blog), 3)
                    context['random_blog'] = random_blog
                    return context
                else:
                    context = super().get_context_data(**kwargs)
                    context['all_mailings'] = cached_context['all_mailings']
                    context['active_mailings'] = cached_context['active_mailings']
                    context['unique_clients_list'] = cached_context['unique_clients_list']
                    all_blog = Blog.objects.all()
                    random_blog = random.sample(list(all_blog), 3)
                    context['random_blog'] = random_blog
                return context


class MessageListView(ListView):
    model = Message
    extra_context = {
            'title': "Все письма",
    }
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(message_owner=self.request.user)
        return queryset


class MessageDetailView(DetailView):
    model = Message

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        message_item = Message.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{message_item.title}'

        return context_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.message_owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.message_owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
            'title': "Все клиенты",
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client_owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.client_owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.client_owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class ClientDetailView(DetailView):
    model = Client


class MailingOptionsCreateView(LoginRequiredMixin, CreateView):
    model = MailingOptions
    form_class = MailingForm
    success_url = reverse_lazy('mailings:message_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:register')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Метод получения данных из базы"""
        queryset = super().get_queryset()
        queryset = queryset.filter(mailing_owner=self.request.user.id)
        return queryset

    def form_valid(self, form):
        self.object = form.save()
        self.object.mailing_owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingOptionsDetailView(LoginRequiredMixin, DetailView):
    model = MailingOptions
    form_class = MailingForm
    success_url = reverse_lazy('mailings:message_list')


class MailingOptionsListView(LoginRequiredMixin, ListView):
    model = MailingOptions
    extra_context = {
            'title': "Все рассылки",
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager'):
            queryset = queryset.all()
        else:
            queryset = queryset.filter(mailing_owner=self.request.user)
        return queryset


class MailingOptionsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingOptions
    success_url = reverse_lazy('mailings:options_list')


class MailingOptionsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingOptions
    form_class = MailingForm
    success_url = reverse_lazy('mailings:options_list')

    def form_valid(self, form):
        send_params = form.save()
        self.model.send_status = send_params.send_status

        send_params.save()
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager'):
            return MailingManagerForm
        return MailingOptionsForm


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client=self.request.user)
        return queryset