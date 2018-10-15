from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

months = {
    1: _('January'),
    2: _('February'),
    3: _('March'),
    4: _('April'),
    5: _('May'),
    6: _('June'),
    7: _('July'),
    8: _('August'),
    9: _('September'),
    10: _('October'),
    11: _('November'),
    12: _('December'),
}

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except KeyError:
        return None

@register.filter
def humanize_month(integer):
    months = {
        1: _('January'),
        2: _('February'),
        3: _('March'),
        4: _('April'),
        5: _('May'),
        6: _('June'),
        7: _('July'),
        8: _('August'),
        9: _('September'),
        10: _('October'),
        11: _('November'),
        12: _('December'),
    }
    try:
        return months[integer]
    except KeyError:
        return months[int(integer)]

def has_children(page):
    return page.featured_page.specific.get_children().exists()

@register.inclusion_tag('tags/featured_pages.html', takes_context=True)
def get_featured_pages(context, calling_page, num_children=3):
    """
    Will return featured pages linked through the
    base.HomePageFeatureRelationship model. If the page has children
    (like Blog or a Gallery), it will render the children as specified
    by num_children; if it does not, it will render a link to the page
    and use an image if available.

    Keyword arguments:
    context -- calling page context, passed automatically
    calling_page -- calling page
    num_children -- number of child pages to render. Default 3.
    """
    featured_pages = []
    for featured_page in calling_page.featured_pages:
        if has_children(featured_page):
            featured_pages.append({
                'obj': featured_page,
                'page': featured_page.featured_page,
                'children': featured_page.featured_page.specific.get_children(
                    ).live().order_by('-last_published_at')[:num_children],
                'style': featured_page.style
            })
        else:
            featured_pages.append({
                'obj': featured_page,
                'page': featured_page.featured_page,
                'style': featured_page.style
            })

    return {
        'featured_pages': featured_pages,
        'request': context['request'],
    }
