from .models import (
    CaptchaFormPage,
    FormPage,
    FooterText,
    StandardPage,
    People,
    HomePage,
)
from .blocks import (
    BaseStreamBlock,
    BlockQuote,
    HeadingBlock,
    ImageBlock,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


# @register(ImageBlock)
# class ImageBlockTR(TranslationOptions):
#     fields = ('caption',)


@register(People)
class PeopleTR(TranslationOptions):
    fields = ('job_title',)


@register(StandardPage)
class StandardPageTR(TranslationOptions):
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