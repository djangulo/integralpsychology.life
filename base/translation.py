from .models import (
    CaptchaFormPage,
    FormPage,
    FooterText,
    StandardPage,
    People,
    PeopleIndexPage,
    HomePage,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(People)
class PeopleTR(TranslationOptions):
    fields = ('job_title', 'bio')


@register(StandardPage)
class StandardPageTR(TranslationOptions):
    fields = ('introduction',)

@register(PeopleIndexPage)
class PeopleIndexPageTR(TranslationOptions):
    fields = ('introduction',)


@register(FooterText)
class FooterTextTR(TranslationOptions):
    fields = ('body',)


@register(FormPage)
class FormPageTR(TranslationOptions):
    fields = (
        'body',
        'thank_you_text',
    )

@register(CaptchaFormPage)
class CaptchaFormPageTR(TranslationOptions):
    fields = (
        'thank_you_text',
    )


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'hero_text',
        'hero_cta',
        'promo_title',
        'promo_text',
        'featured_section_1_title',
        'featured_section_2_title',
        'featured_section_3_title',
    )
