from .models import (
    FormPage,
    FooterText,
    StandardPage,
    People,
    HomePage
)
from .blocks import (
    BaseStreamBlock,
    BlockQuote,
    HeadingBlock,
    ImageBlock,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(People)
class BlogIndexPageTR(TranslationOptions):
    fields = ('job_title',)


@register(StandardPage)
class BlogPageTR(TranslationOptions):
    fields = ('introduction', 'body',)


@register(FooterText)
class BlogPageGalleryImageTR(TranslationOptions):
    fields = ('body',)


@register(FormPage)
class BlogTagIndexPageTR(TranslationOptions):
    fields = (
        'body',
        'thank_you_text',
    )


@register(HomePage)
class BlogTagIndexPageTR(TranslationOptions):
    fields = (
        'hero_text',
        'hero_cta',
        'promo_title',
        'promo_text',
        'featured_section_1_title',
        'featured_section_2_title',
        'featured_section_3_title',
    )


# @register(ImageBlock)
# class ImageBlockTR(TranslationOptions):
#     fields = ('caption')


