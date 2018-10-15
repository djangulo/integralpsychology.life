from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import (
    CaptchaFormField,
    FormPage,
    FooterText,
    HomePage,
    HomePageFeatureRelationship,
    StyleSnippet,
    StandardPage,
    People,
    PeopleIndexPage,
)


@register(People)
class PeopleTR(TranslationOptions):
    fields = ('job_title', 'bio')

@register(StyleSnippet)
class PeopleTR(TranslationOptions):
    pass

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
        'thank_you_text',
    )

@register(CaptchaFormField)
class CaptchaFormFieldTR(TranslationOptions):
    fields = ('label', 'placeholder',)


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'hero_text',
        'hero_cta',
        'promo_title',
        'promo_text',
    )


@register(HomePageFeatureRelationship)
class HomePageFeatureRelationshipTR(TranslationOptions):
    fields = (
        'title',
        'message',
    )
