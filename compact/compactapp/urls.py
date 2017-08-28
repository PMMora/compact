from django.conf.urls import url
#, include

from .views import home
from .views import results_simple
from .views import results_advanced
from .views import error_page
from .views import about
from .views import user_manual
from .views import faq
from .views import home_screen
#from rest_framework import routers
#from compact import views

#router = routers.DefaultRouter()
#router.register(r'home', views.home_screen)
#router.register(r'groups', views.GroupViewSet)
#router.register(r'post', views.PostViewSet)

urlpatterns = [
    url(r'^$', home, name="home"),  # Add this line
    url(r'home^s', home, name="home"),
    url(r'results_simple^s', results_simple, name="results_simple"),
    url(r'results_advanced^s', results_advanced, name="results_advanced"),
    url(r'error_page^s', error_page, name="error_page"),
    url(r'about^s', about, name="about"),
    url(r'user_manual^s', user_manual, name="user_manual"),
    url(r'faq^s', faq, name="faq"),
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^accounts/', include('allauth.urls')),
    #url(r'^admin', include('admin.site.urls'))
]