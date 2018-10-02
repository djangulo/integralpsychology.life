from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from django.utils.translation import gettext_lazy as _

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items_en',
        on_delete=models.CASCADE
    )

class BlogPageTagES(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        verbose_name='tagggggs',
        related_name='tagged_items_es',
        on_delete=models.CASCADE,
        help_text='Listado separado por comas de tags'
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags_en = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
        related_name='posts_en',
    )
    tags_es = ClusterTaggableManager(
        through=BlogPageTagES,
        blank=True,
        related_name='posts_es',
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags_en'),
            FieldPanel('tags_es'),
        ], heading='Blog information'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True,
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get(_('tag'))
        blogpages_en = BlogPage.objects.filter(tags_en__name=tag)
        blogpages_es = BlogPage.objects.filter(tags_es__name=tag)
        context = super().get_context(request)
        context['blogpages_en'] = blogpages_en
        context['blogpages_es'] = blogpages_es
        return context


