from .models import (
    Contact,
    ContactMessage,
    ContactFormPage,
    ContactFormField,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Contact)
class ContactTR(TranslationOptions):
    pass
    # fields = ('intro',)


@register(ContactMessage)
class ContactMessageTR(TranslationOptions):
    pass

@register(ContactFormPage)
class ContactFormPageTR(TranslationOptions):
    fields = ('intro', 'thank_you_text',)

@register(ContactFormField)
class ContactFormFieldTR(TranslationOptions):
    fields = ('label',)
