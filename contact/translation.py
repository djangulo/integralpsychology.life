from .models import (
    Contact,
    ContactMessage,
    ContactFormPage,
    ContactCaptchaFormField,
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
    fields = ('thank_you_text',)

@register(ContactCaptchaFormField)
class ContactCaptchaFormFieldTR(TranslationOptions):
    fields = ('label',)
