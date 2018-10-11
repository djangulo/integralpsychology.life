import django.forms
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
  AbstractFormField, FORM_FIELD_CHOICES)
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CaptchaFormBuilder(FormBuilder):
    # create a function that returns an instanced Django form field
    # function name must match create_<field_type_key>_field

    def _get_language_suffix(self):
        """
        Returns an empty string if language is the default one,
        otherwise returns the actual language string (to be used in
        getattr).
        """
        if get_language() == settings.LANGUAGE_CODE:
            return ''
        return '_%s' % get_language()

    def _get_suffixed_string(self, s):
        return '%s%s' % (s,self._get_language_suffix(),)

    def _get_attrs_dict(self, field):
        if field.additional_attrs is not None:
            return self._normalize_attrs_dict(
                dict(
                    map(lambda y: tuple(y.split('=')),
                        map(lambda x: x,
                            field.additional_attrs.split(',')))),
                field
            )
        return {}

    def _get_class_list(self, field):
        if field.additional_classes is not None:
            return list(map(lambda x: slugify(x.strip()),
                            field.additional_classes.split(',')))
        return []

    def _normalize_attrs_dict(self, d, field=None):
        dd = d.copy()
        # import pdb; pdb.set_trace()
        try:
            classlist = dd['class']
        except KeyError:
            classlist = ''
        for k, v in dd.items():
            if v == 'true':
                dd[k] = True
            if v == 'false':
                dd[k] = False
            dd[slugify(k)] = dd.pop(k)

        if field is not None:
            if hasattr(field, self._get_suffixed_string('placeholder')):
                dd['placeholder'] = getattr(
                    field,
                    self._get_suffixed_string('placeholder'),
                    ''
                )
            else:
                dd['placeholder'] = d['placeholder']
            dd['class'] = (
                classlist + ' '+' '.join(self._get_class_list(field))
            ).strip()
        return dd
            

    def create_singleline_field(self, field, options):
        # TODO: This is a default value - it may need to be changed
        return django.forms.CharField(
            widget=django.forms.TextInput(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_multiline_field(self, field, options):
        return django.forms.CharField(
            widget=django.forms.Textarea(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_date_field(self, field, options):
        return django.forms.DateField(
            widget=django.forms.DateInput(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_datetime_field(self, field, options):
        return django.forms.DateTimeField(
            widget=django.forms.DateTimeInput(
                attrs=self._get_attrs_dict(field)
            ),
            **options
        )

    def create_email_field(self, field, options):
        return django.forms.CharField(
            widget=django.forms.EmailInput(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_url_field(self, field, options):
        return django.forms.CharField(
            widget=django.forms.URLInput(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_number_field(self, field, options):
        return django.forms.DecimalField(
            widget=django.forms.NumberInput(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_dropdown_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(',')
        )
        return django.forms.ChoiceField(
            widget=django.forms.Select(attrs=self._get_attrs_dict(field)),
            **options
        )

    def create_multiselect_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(',')
        )
        return django.forms.MultipleChoiceField(
            widget=django.forms.SelectMultiple(
                attrs=self._get_attrs_dict(field)
            ),
            **options
        )

    def create_radio_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(',')
        )
        return django.forms.ChoiceField(
            widget=django.forms.RadioSelect(
                attrs=self._get_attrs_dict(field)
            ),
            **options
        )

    def create_checkboxes_field(self, field, options):
        options['choices'] = [(x.strip(), x.strip()) for x in field.choices.split(',')]
        options['initial'] = [x.strip() for x in field.default_value.split(',')]
        return django.forms.MultipleChoiceField(
            widget=django.forms.CheckboxSelectMultiple(
                attrs=self._get_attrs_dict(field),
            ), **options
        )

    def create_checkbox_field(self, field, options):
        return django.forms.BooleanField(
            attrs=self._get_attrs_dict(field),
            **options
        )

    def create_hidden_field(self, field, options):
        return django.forms.CharField(
            widget=django.forms.HiddenInput(
                attrs=self._get_attrs_dict(field)
            ),
            **options
        )

    def create_recaptchav2_field(self, field, options):
        return ReCaptchaField(widget=ReCaptchaWidget(), **options)

    # def get_field_options(self, field):
    #     options = {}
    #     options['label'] = field.label
    #     options['hide_label'] = field.hide_label
    #     options['help_text'] = field.help_text
    #     options['required'] = field.required
    #     options['initial'] = field.default_value
    #     return options
