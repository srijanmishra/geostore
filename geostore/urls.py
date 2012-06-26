from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # openid urls
	# url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    # url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
	# url(r'^openid/', include('django_openid_auth.urls')),
	
	# auth url
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
	
	# admin urls
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# kestrel generic urls
	url(r'^$', 'geostore.core.invoke.run'),
	url(r'^(?P<page>[\w+\/]+)?\.?(?P<format>\w+)?/?$', 'geostore.core.invoke.run'),
	url(r'^(?P<service>\w+)/(?P<id>\d+)?\.?(?P<format>\w+)?/?$', 'geostore.core.invoke.run')
)
