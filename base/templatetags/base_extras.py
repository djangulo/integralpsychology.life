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
    return dictionary.get(key)

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
