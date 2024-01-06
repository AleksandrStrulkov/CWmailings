from django.urls import reverse_lazy

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.forms import MessageForm, ClientForm, MailingForm
from mailings.models import MailingOptions, Client, Message


class MailingTemplateView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['all_mailings'] = MailingOptions.objects.all().count()
        context_data['active_mailings'] = MailingOptions.objects.filter(is_active=True).count()
        context_data['unique_clients_list'] = Client.objects.all().distinct('client_email').count()

        return context_data


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        message_item = Message.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{message_item.title}'

        return context_data


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:home')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:home')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:home')


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class ClientDetailView(DetailView):
    model = Client


class MailingOptionsCreateView(CreateView):
    model = MailingOptions
    form_class = MailingForm
    success_url = reverse_lazy('mailings:message_list')


class MailingOptionsDetailView(DetailView):
    model = MailingOptions
    form_class = MailingForm
    success_url = reverse_lazy('mailings:message_list')


class MailingOptionsListView(ListView):
    model = MailingOptions


class MailingOptionsDeleteView(DeleteView):
    model = MailingOptions
    success_url = reverse_lazy('mailings:options_list')

