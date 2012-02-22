from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'casei.views.login'),
    url(r'^signup/$', 'casei.views.signup'),
    url(r'^do_signup/$', 'casei.views.do_signup'),
    url(r'^signup_thanks/$', 'casei.views.signup_thanks'),
    url(r'^do_logout/$', 'casei.views.do_logout'),
    url(r'^ncaa/', include('casei.ncaacards.urls')),
    # Examples:
    # url(r'^$', 'casei.views.home', name='home'),
    # url(r'^casei/', include('casei.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
