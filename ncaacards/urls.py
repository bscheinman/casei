from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'casei.ncaacards.views.home'),
    url(r'^do_logout/$', 'casei.ncaacards.views.do_logout'),
    url(r'^game/([0-9]+)/$', 'casei.ncaacards.views.game_home'),
    url(r'^game/([0-9]+)/marketplace/$', 'casei.ncaacards.views.marketplace'),
    url(r'^game/([0-9]+)/entry/([0-9]+)/$', 'casei.ncaacards.views.entry_view'),
    url(r'^game/([0-9]+)/team/([0-9]+)/$', 'casei.ncaacards.views.game_team_view'),
    url(r'^game/([0-9]+)/team/([a-zA-Z]+)/$', 'casei.ncaacards.views.game_team_view'),
    url(r'^game/([0-9]+)/create_offer/$', 'casei.ncaacards.views.create_offer'),
    url(r'^game/([0-9]+)/make_offer/$', 'casei.ncaacards.views.make_offer'),
    url(r'^game/([0-9]+)/offer/([0-9]+)/$', 'casei.ncaacards.views.offer_view'),
    url(r'^team/([0-9]+)/$', 'casei.ncaacards.views.team_view'),
    url(r'^team/([a-zA-Z]+)/$', 'casei.ncaacards.views.team_view'),
    # Examples:
    # url(r'^$', 'casei.views.home', name='home'),
    # url(r'^casei/', include('casei.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
