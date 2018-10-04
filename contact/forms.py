from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import (
#     ButtonHolder,
#     Field,
#     Fieldset,
#     HTML,
#     Button,
#     Layout,
#     Submit,
#     Div,
# )

from .models import (
    ContactDetails,
    ContactMessage,
    ContactFormPage,
)

class SendMessageForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=ContactDetails.objects.all()
    )
    message = forms.CharField(widget=forms.Textarea())

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['message'].widget.attrs.update({'autofocus': True})
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'send-email-form'
    #     self.helper.form_method = 'post'
    #     # self.helper.form_action = reverse('contact:send_email')
    #     self.helper.html5_required = False
    #     self.helper.form_tag = True
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             HTML(_('<h1 class="h1">Send email</h1>')),
    #             Field(
    #                 'recipient',
    #                 id='recipient',
    #                 css_class='form-control dropdown',
    #             ),
    #             Field(
    #                 'message',
    #                 id='message',
    #                 css_class='form-control',
    #             ),
    #             ButtonHolder(
    #                 Submit('submit', _('Submit'), css_class='btn btn-primary'),
    #                 Button('cance', _('Cancel'), css_class='btn btn-default'),
    #             )
    #         )
    #     )

class ContactForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), required=True)
    last_name = forms.CharField(label=_('Last name'), required=True)
    email = forms.CharField(label=_('Email'), required=True)
    phone = forms.CharField(label=_('Phone number'), required=False)
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea()
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['first_name'].widget.attrs.update({'autofocus': True})
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'contact-form'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = reverse('contact:contact_form')
    #     self.helper.html5_required = False
    #     self.helper.form_tag = True
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             HTML(_('<h1 class="h1">Send email</h1>')),
    #             Div(
    #                 Field(
    #                     'first_name',
    #                     css_class='form-control',
    #                     wrapper_class='col-sm-12 col-md-6 mb-3'
    #                 ),
    #                Field(
    #                     'last_name',
    #                     css_class='form-control',
    #                     wrapper_class='col-sm-12 col-md-6 mb-3'
    #                 ),
    #                Field(
    #                     'email',
    #                     css_class='form-control',
    #                     wrapper_class='col-sm-12 col-md-6 mb-3'
    #                 ),
    #                Field(
    #                     'phone',
    #                     css_class='form-control',
    #                     wrapper_class='col-sm-12 col-md-6 mb-3'
    #                 ),
    #                 css_class='form-row'
    #             ),
    #             Div(
    #                 Field(
    #                     'message',
    #                     css_class='form-control',
    #                     wrapper_class='col-sm-12',
    #                 ),
    #                 css_class='form-row',
    #             ),
    #             ButtonHolder(
    #                 Submit('submit', _('Submit'), css_class='btn btn-primary'),
    #                 Button('cancel', _('Cancel'), css_class='btn btn-default'),
    #                 css_class='mt-2'
    #             )
    #         )
    #     )