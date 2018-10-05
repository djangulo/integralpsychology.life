from django import forms
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
  AbstractFormField, FORM_FIELD_CHOICES)
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CaptchaFormBuilder(FormBuilder):
    # create a function that returns an instanced Django form field
    # function name must match create_<field_type_key>_field
    def create_recaptchav2_field(self, field, options):
        # return `forms.GenericIPAddressField(**options)` not `forms.SlugField`
        # returns created a form field with the options passed in
        return ReCaptchaField(widget=ReCaptchaWidget(), **options)
