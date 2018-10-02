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
    fields = ('intro',)


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = ('intro', 'body',)


@register(BlogPageGalleryImage)
class BlogPageGalleryImageTR(TranslationOptions):
    fields = ('caption',)

@register(BlogTagIndexPage)
class BlogTagIndexPageTR(TranslationOptions):
    pass


