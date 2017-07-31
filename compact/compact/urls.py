from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'compact.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	#url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^',include('compactapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
