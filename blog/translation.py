from .models import (
    BlogIndexPage,
    BlogPage,
    BlogPageGalleryImage,
    BlogTagIndexPage,
)
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    fields = ('introduction',)


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = ('introduction', 'body',)


@register(BlogPageGalleryImage)
class BlogPageGalleryImageTR(TranslationOptions):
    fields = ('caption',)

@register(BlogTagIndexPage)
class BlogTagIndexPageTR(TranslationOptions):
    pass


