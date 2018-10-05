import json
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _
from wagtail.core.fields import RichTextField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.utils import send_mail
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    AbstractFormSubmission,
    FORM_FIELD_CHOICES,
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from base.blocks import BaseStreamBlock
from base.forms import CaptchaFormBuilder

@register_snippet
class Contact(index.Indexed, ClusterableModel):
    """
    Django model to store Contact objects (related to contact form).
    """
    first_names = models.CharField(
        verbose_name=_('First name(s)'),
        max_length=254,
        blank=False,
        null=False,
    )
    last_names = models.CharField(
        verbose_name=_('Last name(s)'),
        max_length=254,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name=_('Email'),
        blank=False,
        null=False,
    )
    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=15,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
    
    def get_messages(self):
        return self.messages.all()

    @property
    def get_message_count(self):
        return self.messages.count()

    @property
    def get_full_name(self):
        return '%s %s' % (self.first_names, self.last_names,)

    @property
    def get_latest_message(self):
        return self.messages.latest()

    def __str__(self):
        return f'{self.first_names} {self.last_names}: {self.email}'


class ContactMessage(AbstractFormSubmission):
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        related_name='messages',
    )
    message = models.TextField(verbose_name=_('Message'))

    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')
        get_latest_by = 'submit_time'
        ordering = ('-submit_time',)


class ContactCaptchaFormField(AbstractFormField):
    # extend the built in field type choices
    # our field type key will be 'ipaddress'
    CHOICES = FORM_FIELD_CHOICES + (('recaptchav2', 'Google Recaptcha V2'),)

    page = ParentalKey('ContactFormPage', related_name='form_fields')
    # override the field_type field with extended choices
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=CHOICES,
    )


class ContactFormPage(AbstractEmailForm):
    """
    Contact form page that uses wagtail fields. Note that fields
    are locked to first_names, last_names, email, phone & message.
    Users can still build custom forms by using the FormPage model.
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    form_builder = CaptchaFormBuilder
    
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        # InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
        ], "Email"),
    ]

    def get_submission_class(self):
        return ContactMessage
    
    def process_bilingual_form_data(self, form):
        """
        Returns a cleaned_data object with all english keys.
        wagtail-modeltranslation is delivering a cleaned_data object
        with translated-keys.
        """
        keys = list(form.cleaned_data.keys()) # Original keys
        fields = [
            ['first-names', keys[0]],
            ['last-names', keys[1]],
            ['email', keys[2]],
            ['phone', keys[3]],
            ['message', keys[4]],
            ['are-you-a-robot', keys[5]],
        ]
        res = []
        for f in fields:
            try:
                res.append(form.cleaned_data[f[0]]) # Attempt english retrieval first
            except KeyError:
                res.append(form.cleaned_data[f[1]]) # Translated language
        return {f[0]: r for f,r in zip(fields, res)} # Return dict with english keys

    def process_form_submission(self, form):
        # import pdb; pdb.set_trace()
        cleaned_data = self.process_bilingual_form_data(form)
        try:
            contact = Contact.objects.get(email=cleaned_data['email'])
        except Contact.DoesNotExist:
            contact = Contact.objects.create(
                first_names=cleaned_data['first-names'],
                last_names=cleaned_data['last-names'],
                email=cleaned_data['email'],
                phone=cleaned_data['phone'],
            )
        submission = self.get_submission_class().objects.create(
            form_data=json.dumps(cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            contact=contact,
        )
        if self.to_address:
            self.send_mail(form)
        return submission

    def send_mail(self, form):
        cleaned_data = self.process_bilingual_form_data(form)
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))

        content = '\n'.join(content)
        subject = "Message from: %(fname)s %(lname)s <%(email)s>" % {
            'fname': cleaned_data['first-names'],
            'lname': cleaned_data['last-names'],
            'email': cleaned_data['email'],
        }
        send_mail(subject, content, addresses, self.from_address,)

    def save(self, *args, **kwargs):
        super().save()
        field_list = list(
            self.form_fields.all().values_list('label', flat=True)
        )
        if 'First name(s)' not in field_list:
            ContactCaptchaFormField.objects.create(
                label='First name(s)',
                label_es='Nombre(s)',
                field_type='singleline',
                required=True,
                page=self
            )
        if 'Last name(s)' not in field_list:
            ContactCaptchaFormField.objects.create(
                label='Last name(s)',
                label_es='Apellido(s)',
                field_type='singleline',
                required=True,
                page=self
            )
        if 'Email' not in field_list:
            ContactCaptchaFormField.objects.create(
                label='Email',
                label_es='Correo electrónico',
                field_type='email',
                required=True,
                page=self,
            )
        if 'Phone' not in field_list:
            ContactCaptchaFormField.objects.create(
                label='Phone',
                label_es='Teléfono',
                field_type='singleline',
                required=False,
                page=self,
            )
        if 'Message' not in field_list:
            ContactCaptchaFormField.objects.create(
                label='Message',
                label_es='Mensaje',
                field_type='multiline',
                required=True,
                page=self,
            )
        if 'recaptchav2' not in list(
            self.form_fields.all().values_list('field_type', flat=True)
        ):
            ContactCaptchaFormField.objects.create(
                label='',
                label_es='',
                field_type='recaptchav2',
                required=True,
                page=self,
            )

        super().save(*args, **kwargs)
