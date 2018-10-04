from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from contact import models
from contact.forms import SendMessageForm, ContactForm

class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = 'contact/contact_email_form.html'

class ContactListView(LoginRequiredMixin, generic.ListView):
    model = models.ContactDetails

class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.ContactDetails

class ContactMessageListView(LoginRequiredMixin, generic.ListView):
    model = models.ContactMessage

class ContactMessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.ContactMessage

class SendContactMessageView(LoginRequiredMixin, generic.FormView):
    form_class = SendMessageForm
    template_name = 'contact/contact_email_form.html'

# Create your views here.
