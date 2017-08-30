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
    url(r'^home/', 'compactapp.views.home', name='home'),
    url(r'^results_simple', 'compactapp.views.results_simple', name='results_simple'),
    url(r'^results_simple/', 'compactapp.views.results_simple', name='results_simple'),
    url(r'^results_advanced', 'compactapp.views.results_advanced', name='results_advanced'),
    url(r'^results_advanced/', 'compactapp.views.results_advanced', name='results_advanced'),
    url(r'^error_page', 'compactapp.views.error_page', name='error_page'),
    url(r'^about', 'compactapp.views.about', name='about'),
    url(r'^user_manual', 'compactapp.views.user_manual', name='user_manual'),
    url(r'^faq', 'compactapp.views.faq', name='faq')
    ]
