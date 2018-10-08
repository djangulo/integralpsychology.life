# from taggit.models import Tag
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import (
    BlogIndexPage,
    BlogPage,
    BlogPageGalleryImage,
)


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    fields = ('introduction',)


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = ('introduction', 'subtitle',)


@register(BlogPageGalleryImage)
class BlogPageGalleryImageTR(TranslationOptions):
    fields = ('caption',)
