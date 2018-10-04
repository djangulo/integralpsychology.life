from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _, get_language
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from base.blocks import BaseStreamBlock

class BlogPeopleRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.
    We have created a two way relationship between BlogPage and People using
    the ParentalKey and ForeignKey
    """
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'base.People', related_name='person_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('people')
    ]



class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items_en',
        on_delete=models.CASCADE
    )

class BlogPageTagES(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        verbose_name='tags_es',
        related_name='tagged_items_es',
        on_delete=models.CASCADE,
        help_text='Listado separado por comas de tags'
    )


class BlogPage(Page):
    subtitle = models.CharField(blank=True, max_length=255)
    date_published = models.DateField(
        "Date article published",
        blank=True,
        null=True
        )
    introduction = models.CharField(max_length=250)
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    tags_en = ClusterTaggableManager(
        verbose_name='Tags',
        through=BlogPageTag,
        blank=True,
        related_name='posts_en',
        help_text='A comma-separated list of tags for the english'\
                  ' version.'
    )
    tags_es = ClusterTaggableManager(
        verbose_name='Tags [ES] (Etiquetas)',
        through=BlogPageTagES,
        blank=True,
        related_name='posts_es',
        help_text='Listado separado por comas de etiquetas para la'\
                  ' versión en español.',
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname='full'),
        FieldPanel('introduction', classname='full'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('date_published'),
            FieldPanel('tags_en'),
            FieldPanel('tags_es'),
        ], heading='Blog information'),
        InlinePanel('gallery_images', label='Gallery images'),
    ]

    def authors(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        authors = [
            n.people for n in self.blog_person_relationship.all()
        ]
        return authors

    @property
    def get_en_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags_en.all()
        for tag in tags:
            tag.url = '/'+'/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    @property
    def get_es_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags_es.all()
        for tag in tags:
            tag.url = '/'+'/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['BlogIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []



class BlogIndexPage(RoutablePageMixin, Page):
    """
    Index page for blogs.
    We need to alter the page model's context to return the child page objects,
    the BlogPage objects, so that it works as an index page
    RoutablePageMixin is used to allow for a custom sub-URL for the tag views
    defined above.
    """
    introduction = RichTextField(blank=True)
    subpage_types = ['BlogPage']
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live().order_by('-date_published')
        return context

    @route('^tags/$', name='tag_archive')
    @route('^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            if get_language() == 'en':
                tags += post.get_en_tags
            else:
                tags += post.get_es_tags
        tags = sorted(set(tags))
        return tags

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


# @register_snippet
# class BlogCategory(models.Model):
#     name = models.CharField(max_length=255)
#     icon = models.ForeignKey(
#         'wagtailimages.Image', null=True, blank=True,
#         on_delete=models.SET_NULL, related_name='+'
#     )

#     panels = [
#         FieldPanel('name'),
#         ImageChooserPanel('icon'),
#     ]

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = 'blog categories'