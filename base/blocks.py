from django.utils.translation import gettext_lazy as _
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StaticBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    caption_es = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    heading_text_es = CharBlock(classname="title", required=False)
    size = ChoiceBlock(choices=[
        ('', _('Select a header size')),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class ParagraphBlock(StructBlock):
    body = RichTextBlock(classname='body', required=True)
    body_es = RichTextBlock(classname='body', required=False)

    class Meta:
        icon = "fa-paragraph"
        template = "blocks/paragraph_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock(required=True)
    text_es = TextBlock(required=False)
    attribute_name = CharBlock(
        blank=True, required=False, label='Author; e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


class CaptionEmbedBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to embed and add a caption.
    """
    caption = TextBlock()
    caption_es = TextBlock()
    embed = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")

    class Meta:
        icon = "fa-s15"
        template = 'blocks/caption_embed_block.html'


class MessageDividerBlock(StructBlock):

    message = TextBlock()
    message_es = TextBlock()

    class Meta:
        icon = "fa-square"
        template = 'blocks/message_divider_block.html'


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = ParagraphBlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")
    divider_block = MessageDividerBlock()
