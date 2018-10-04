from django.conf.urls import url

from contact import views

app_name = 'contact'
urlpatterns = [
    url(r'^$', views.ContactFormView.as_view(), name='contact_form'),
    url(r'^list/$', views.ContactListView.as_view(), name='contact_list'),
    url(r'^(?P<pk>\d+)/$', views.ContactDetailView.as_view(), name='contact_detail'),
    url(r'^(?P<pk>\d+)/send_email/$', views.SendContactMessageView.as_view(), name='send_email'),
    url(r'^messages/$', views.ContactMessageListView.as_view(), name='message_list'),
    url(r'^messages/(?P<pk>\d+)/$', views.ContactMessageDetailView.as_view(), name='message_detail'),
]