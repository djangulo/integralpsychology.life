import json
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
)
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.utils import send_mail
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    AbstractFormSubmission,
    FORM_FIELD_CHOICES,
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from snowpenguin.django.recaptcha2.fields import ReCaptchaField


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
        return f'{self.first_name} {self.last_name}: {self.email}'


class ContactMessage(AbstractFormSubmission):
    contact = models.ForeignKey(
        'contact.Contact',
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


class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactFormPage',
                       on_delete=models.CASCADE,
                       related_name='form_fields')
    CHOICES = FORM_FIELD_CHOICES + (('google_recaptchav2', 'Google Recaptcha V2'),)
    field_type = models.CharField(
        verbose_name=_('field type'),
        max_length=16,
        choices=CHOICES
    )

    def __str__(self):
        return '%(page)s: %(label)s - %(type)s' % {
            'page': self.page.title or None,
            'type': self.field_type,
            'label': self.label,
        }

class ContactFormBuilder(FormBuilder):
    def create_google_recaptchav2_field(self, field, options):
        return ReCaptchaField(**options)

class ContactFormPage(AbstractEmailForm):
    """
    Contact form page that uses wagtail fields. Note that fields
    are locked to first_names, last_names, email, phone & message.
    Users can still build custom forms by using the FormPage model.
    """
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    form_builder = ContactFormBuilder

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
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

    def process_form_submission(self, form):
        try:
            contact = Contact.objects.get(email=form.cleaned_data['email'])
        except Contact.DoesNotExist:
            contact = Contact.objects.create(
                first_names=form.cleaned_data['first_names'],
                last_names=form.cleaned_data['last_names'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
            )
        submission = self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            contact=contact,
            message=form.cleaned_data['message'],
        )
        if self.to_address:
            self.send_mail(form)
        return submission

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))

        content = '\n'.join(content)
        subject = "Message from: %(fname)s %(lname)s <%(email)s>" % {
            'fname': form.cleaned_data['first_names'],
            'lname': form.cleaned_data['last_names'],
            'email': form.cleaned_data['email'],
        }
        send_mail(subject, content, addresses, self.from_address,)

    def save(self, *args, **kwargs):
        super().save()
        ContactFormField.objects.create(
            label='First name(s)',
            label_es='Nombre(s)',
            field_type='singleline',
            required=True,
            page=self
        )
        ContactFormField.objects.create(
            label='Last name(s)',
            label_es='Apellido(s)',
            field_type='singleline',
            required=True,
            page=self
        )
        ContactFormField.objects.create(
            label='Email',
            label_es='Correo electrónico',
            field_type='email',
            required=True,
            page=self,
        )
        ContactFormField.objects.create(
            label='Phone',
            label_es='Teléfono',
            field_type='singleline',
            required=False,
            page=self,
        )
        ContactFormField.objects.create(
            label='Message',
            label_es='Mensaje',
            field_type='multiline',
            required=True,
            page=self,
        )
        super().save(*args, **kwargs)
