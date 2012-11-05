from django.conf.urls.defaults import *
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^contactes/', include('django-registration-jaem.contacts.urls')),    
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'contacts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
    (r'^$', RedirectView.as_view(url='/login/')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # (r'^contactes/comments/',      include('django.contrib.comments.urls')),
    (r'^contactes/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'public/contactes/css/','show_indexes': True}),
    (r'^contactes/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'public/contactes/js/','show_indexes': True}),
    (r'^contactes/img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'public/contactes/img/','show_indexes': True}),
)
