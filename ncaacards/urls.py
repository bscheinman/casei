from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'casei.ncaacards.views.home'),
    url(r'^game/([0-9]+)/$', 'casei.ncaacards.views.game_home'),
    url(r'^game/([0-9]+)/marketplace/$', 'casei.ncaacards.views.marketplace'),
    url(r'^game/([0-9]+)/leaderboard/$', 'casei.ncaacards.views.leaderboard'),
    url(r'^game/([0-9]+)/entry/([0-9]+)/$', 'casei.ncaacards.views.entry_view'),
    url(r'^game/([0-9]+)/team/([0-9]+)/$', 'casei.ncaacards.views.game_team_view'),
    url(r'^game/([0-9]+)/team/([a-zA-Z]+)/$', 'casei.ncaacards.views.game_team_view'),
    url(r'^game/([0-9]+)/create_offer/$', 'casei.ncaacards.views.create_offer'),
    url(r'^game/([0-9]+)/make_offer/$', 'casei.ncaacards.views.make_offer'),
    url(r'^game/([0-9]+)/do_trade/$', 'casei.ncaacards.views.do_trade'),
    url(r'^game/([0-9]+)/offer/([0-9]+)/$', 'casei.ncaacards.views.offer_view'),
    url(r'^game/([0-9]+)/offer/([0-9]+)/accept/$', 'casei.ncaacards.views.accept_offer'),
    url(r'^game/([0-9]+)/offer/([0-9]+)/cancel/$', 'casei.ncaacards.views.cancel_offer'),
    url(r'^team/([0-9]+)/$', 'casei.ncaacards.views.team_view'),
    url(r'^team/([a-zA-Z]+)/$', 'casei.ncaacards.views.team_view'),
    url(r'^create_game/$', 'casei.ncaacards.views.create_game'),
    url(r'^game_list/$', 'casei.ncaacards.views.game_list'),
    url(r'^do_create_game/$', 'casei.ncaacards.views.do_create_game'),
    url(r'^join_game/$', 'casei.ncaacards.views.join_game'),
    # Examples:
    # url(r'^$', 'casei.views.home', name='home'),
    # url(r'^casei/', include('casei.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
