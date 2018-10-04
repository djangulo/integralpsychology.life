from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from contact.models import Contact

'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:
INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)
or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html
This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''



class ContactsModelAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Contacts'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-address-book'  # change as required
    list_display = (
        'first_names',
        'last_names',
        'email',
        'phone',
        'get_message_count',
    )


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(ContactsModelAdmin)