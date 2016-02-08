from django.conf.urls import include, url, patterns

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^index/$', 'signups.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^thank-you/$', 'signups.views.thankyou', name='thankyou'),
    url(r'^about-us/$', 'signups.views.aboutus', name='aboutus'),
    url(r'^main/$', 'signups.views.main', name='main'),
    url(r'^profile/$', 'signups.views.profile', name='profile'),
    url(r'^friend/$', 'signups.views.friend', name='friend'),     
    url(r'^friend-profile/$', 'signups.views.friend_profile', name='friend_profile'),    
    url(r'^friend-uprofile/(?P<target_username>[\w|\W]+)/$', 'signups.views.friend_profile', name='friend_profile'), 
    url(r'^edit-profile/$', 'signups.views.edit_profile', name='edit_profile'),
    url(r'^friend-confirm/$', 'signups.views.friend_confirm', name='friend_confirm'),
    url(r'^account-confirm/$', 'signups.views.account_confirm', name='account_confirm'),   
    url(r'^create-account/$', 'signups.views.create_account', name='create_account'),
    url(r'^create-circle/$', 'signups.views.create_circle', name='create_circle'),   
    url(r'^add-circle/$', 'signups.views.add_circle', name='add_circle'),   
    url(r'^friend-request/(?P<target_username>[\w|\W]+)/$', 'signups.views.friend_request', name='friend_request'),
    url(r'^search/(?P<target_username>[\w|\W]+)/$', 'signups.views.search', name='search'),  
    url(r'^circle-profile/(?P<target_username>[\w|\W]+)/$', 'signups.views.circle_profile', name='circle_profile'),
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,
		                    document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,
		                    document_root = settings.MEDIA_ROOT)