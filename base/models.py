from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    FORM_FIELD_CHOICES,
)
from wagtail.documents.models import AbstractDocument, Document, get_document_model
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from .blocks import BaseStreamBlock
from .forms import CaptchaFormBuilder


@register_snippet
class People(index.Indexed, ClusterableModel):
    """
    A Django model to store People objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/base/people/)
    `People` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)
    bio = models.TextField(blank=True, null=True)
    # display_in_page = models.BooleanField(default=False)
    social_linkedin = models.URLField(blank=True, null=True)
    social_github = models.URLField(blank=True, null=True)
    social_facebook = models.URLField(blank=True, null=True)
    social_instagram = models.URLField(blank=True, null=True)
    social_googleplus = models.URLField(blank=True, null=True)
    social_twitter = models.URLField(blank=True, null=True)


    picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('picture'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], _("Name")),
        FieldPanel('job_title'),
        FieldPanel('bio'),
        MultiFieldPanel([
            FieldPanel('social_linkedin'),
            FieldPanel('social_facebook'),
            FieldPanel('social_instagram'),
            FieldPanel('social_twitter'),
            FieldPanel('social_github'),
            FieldPanel('social_googleplus'),
        ], _('Social links'))
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            # pylint: disable=E1101
            return self.image.get_rendition('fill-50x50').img_tag()
        except:
            return ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class PeopleIndexPage(Page):
    introduction = RichTextField(blank=True)
    people = ParentalManyToManyField('People', blank=True)
    
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('people', widget=forms.CheckboxSelectMultiple),
    ]
    subpage_types = []
    parent_page_types = ['HomePage']


# class PeopleDetailPage(Page):


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'


class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = RichTextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
    ]

class StyleDocument(AbstractDocument):

    source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    admin_form_fields = Document.admin_form_fields + (
        'source',
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(StyleDocument, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        self.validate_file_extension()
        super(StyleDocument, self).clean(*args, **kwargs)

    def validate_file_extension(self):
        if self.file_extension not in ('css', 'scss', 'sass'):
            raise ValidationError(
                _('Invalid file extension, must be .css|scss|sass'),
                code='invalid_file',
            )


@register_snippet
class StyleSnippet(index.Indexed, ClusterableModel):
    identifier = models.CharField(
        _('identifier'),
        max_length=254,
    )
    class_name = models.SlugField(
        _('class name'),
        max_length=254,
        help_text=_('Name of the CSS class name that the snippet will'\
                    'be rendered with. Be careful not to choose a cla'\
                    'ss name that will interfere with the rest of the'\
                    ' styles. The same class name needs to match the '\
                    'class defined in the style_file.')
    )
    style_file = models.ForeignKey(
        get_document_model(),
        verbose_name=_('style file'),
        blank=False,
        null=False,
        related_name='+',
        on_delete=models.CASCADE,
        help_text=_('Only filenames ending in .css, .scss or .sass '\
                    'will be processed.')
    )

    panels = [
        FieldPanel('identifier'),
        FieldPanel('class_name'),
        DocumentChooserPanel('style_file'),
    ]

    search_fields = [
        index.SearchField('identifier'),
        index.SearchField('class_name'),
    ]

    def __str__(self):
        return self.identifier

    class Meta:
        verbose_name = _('style snippet')
        verbose_name_plural = _('style snippets')

    def validate_file_extension(self):
        # pylint: disable=E1101
        if self.style_file.file_extension not in ('css', 'scss', 'sass'):
            raise ValidationError(
                _('Invalid file extension, must be .css|scss|sass'),
                code='invalid_file',
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(StyleSnippet, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        self.validate_file_extension()
        super(StyleSnippet, self).clean(*args, **kwargs)


class FeaturedPage(models.Model):
    title = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        help_text=_('Title to display on the Home Page, if left blank'\
                    ', the featured page\'s title will be used')
    )
    slug = models.SlugField(
        max_length=254,
        blank=False,
        null=False,
        help_text=_('Slug to refer to the feature page when calling '\
                    'it through the \'featured_page_single\' template'\
                    ' tag. Required.')
    )
    message = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        help_text=_('Message inviting users to go see this feature')
    )
    featured_page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='feature_home_relationship',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    style = models.ForeignKey(
        'StyleSnippet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Style snippet to use, will use a default style '\
                    'if left blank. Take a look at the default file '\
                    'in \'base/static/scss/default-snippets/default.scss'\
                    ' and other files there for some examples on how '\
                    'to setup the [S]CSS classes.')
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('message'),
        PageChooserPanel('featured_page'),
        SnippetChooserPanel('style'),
    ]

    class Meta:
        abstract = True


class HomePageFeatureRelationship(Orderable, FeaturedPage):
    page = ParentalKey(
        'HomePage',
        related_name='home_feature_relationship',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class HomePage(Page):
    """
    The Home Page. This looks slightly more complicated than it is. You can
    see if you visit your site and edit the homepage that it is split between
    a:
    - Hero area
    - Body area
    - A promotional area
    - Moveable featured site sections
    """
    template = 'base/home_page.html'
    # Hero section of HomePage
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )
    hero_text = models.CharField(
        max_length=255,
        help_text='Write an introduction for the bakery'
        )
    hero_cta = models.CharField(
        verbose_name='Hero CTA',
        max_length=255,
        help_text='Text to display on Call to Action'
        )
    hero_cta_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Hero CTA link',
        help_text='Choose a page to link to for the Call to Action'
    )

    # Body section of the HomePage
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )

    # Promo section of the HomePage
    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Promo image'
    )
    promo_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    promo_text = RichTextField(
        null=True,
        blank=True,
        help_text='Write some promotional copy'
    )

    @property
    def featured_pages(self):
        return self.home_feature_relationship.all()

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('hero_image'),
            FieldPanel('hero_text', classname="full"),
            MultiFieldPanel([
                FieldPanel('hero_cta'),
                PageChooserPanel('hero_cta_link'),
                ])
            ], heading="Hero section"),
        MultiFieldPanel([
            ImageChooserPanel('promo_image'),
            FieldPanel('promo_title'),
            FieldPanel('promo_text'),
        ], heading="Promo section"),
        StreamFieldPanel('body'),
        InlinePanel(
            relation_name='home_feature_relationship',
            heading=_('Featured homepage sections'),
            label=_("Featured_pages"),
            help_text=_('Each of the links selected will have a small'\
                        ' section on the Home Page.'),
            min_num=0,
            max_num=5,
            classname="collapsible"),
    ]

    def __str__(self):
        return self.title

    @property
    def is_home_page(self):
        return True


# class AbstractFormField(Orderable):
#     """
#     Database Fields required for building a Django Form field.
#     """

#     label = models.CharField(
#         verbose_name=_('label'),
#         max_length=255,
#         help_text=_('The label of the form field')
#     )
#     field_type = models.CharField(verbose_name=_('field type'), max_length=16, choices=FORM_FIELD_CHOICES)
#     required = models.BooleanField(verbose_name=_('required'), default=True)
#     choices = models.TextField(
#         verbose_name=_('choices'),
#         blank=True,
#         help_text=_('Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.')
#     )
#     default_value = models.CharField(
#         verbose_name=_('default value'),
#         max_length=255,
#         blank=True,
#         help_text=_('Default value. Comma separated values supported for checkboxes.')
#     )
#     help_text = models.CharField(verbose_name=_('help text'), max_length=255, blank=True)

#     @property
#     def clean_name(self):
#         # unidecode will return an ascii string while slugify wants a
#         # unicode string on the other hand, slugify returns a safe-string
#         # which will be converted to a normal str
#         return str(slugify(str(unidecode(self.label))))

#     panels = [
#         FieldPanel('label'),
#         FieldPanel('help_text'),
#         FieldPanel('required'),
#         FieldPanel('field_type', classname="formbuilder-type"),
#         FieldPanel('choices', classname="formbuilder-choices"),
#         FieldPanel('default_value', classname="formbuilder-default"),
#     ]

#     class Meta:
#         abstract = True
#         ordering = ['sort_order']

class CaptchaFormField(AbstractFormField):
    # extend the built in field type choices
    # our field type key will be 'ipaddress'
    CHOICES = FORM_FIELD_CHOICES + (('recaptchav2', 'Google Recaptcha V2'),)

    page = ParentalKey('FormPage', related_name='form_fields')
    placeholder = models.CharField(
        verbose_name=_('placeholder'),
        max_length=254,
        blank=True,
        help_text=_('Placeholder text. This takes precedence over a '\
                  'placeholder set in additional_attrs.')
    )
    # override the field_type field with extended choices
    additional_classes = models.CharField(
        verbose_name=_('additional classes'),
        max_length=254,
        blank=True,
        null=True,
        help_text='Comma separated list of html classes to pass on to '\
                  'the input element.'
    )
    additional_attrs = models.CharField(
        verbose_name=_('additional attributes'),
        max_length=254,
        blank=True,
        null=True,
        help_text=_('Comma separated list of key-value pairs to add '\
                    'to the input element. Quotes are not'\
                    ' necessary.\n'\
                    'e.g. data-toggle=dropdown,aria-haspopup=true')\
    )
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        # use the choices tuple defined above
        choices=CHOICES
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('label'),
        ], _('Label')),
        FieldPanel('help_text'),
        FieldPanel('placeholder'),
        FieldPanel('required'),
        FieldPanel('field_type', classname="formbuilder-type"),
        FieldPanel('choices', classname="formbuilder-choices"),
        FieldPanel('default_value', classname="formbuilder-default"),
        MultiFieldPanel([
            FieldPanel('additional_classes'),
            FieldPanel('additional_attrs'),
        ], _('Developer options')),
    ]

class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    form_builder = CaptchaFormBuilder
    
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
