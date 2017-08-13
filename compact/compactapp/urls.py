from django.conf.urls import url
#, include
from .views import home_screen
from .views import results
from .views import error_page
#from rest_framework import routers
#from compact import views

#router = routers.DefaultRouter()
#router.register(r'home', views.home_screen)
#router.register(r'groups', views.GroupViewSet)
#router.register(r'post', views.PostViewSet)

urlpatterns = [
    url(r'^$', home_screen, name="home"),  # Add this line
    url(r'results^s', results, name="results"),
    url(r'error_page^s', error_page, name="error_page")
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^accounts/', include('allauth.urls')),
    #url(r'^admin', include('admin.site.urls'))
]