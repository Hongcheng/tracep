from django.conf.urls import patterns, include, url
from views import Home_Page
from amazon.views import Show_Amazon_Price,Amazon_Home_Page
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
	('^$',Home_Page),
	(r'^amazon/$',Amazon_Home_Page),
	(r'^amazon/(.{1,10})/$',Show_Amazon_Price),
    # Examples:
    # url(r'^$', 'tracep.views.home', name='home'),
    # url(r'^tracep/', include('tracep.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
# urlpatterns += staticfiles_urlpatterns()
