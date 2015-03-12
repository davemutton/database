from django.conf.urls import patterns, url,include
from property import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'clients', views.ClientViewSet)


urlpatterns = patterns('',
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
	)