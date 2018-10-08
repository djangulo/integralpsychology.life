from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact


class SendMessageForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=Contact.objects.all()
    )
    message = forms.CharField(widget=forms.Textarea())


class ContactForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), required=True)
    last_name = forms.CharField(label=_('Last name'), required=True)
    email = forms.CharField(label=_('Email'), required=True)
    phone = forms.CharField(label=_('Phone number'), required=False)
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea()
    )
