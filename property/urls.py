from django.conf.urls import patterns, url
from property import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^listing/$', views.listing, name='list'),
	url(r'download/$',views.property_download, name='download'),
	url(r'^new$', views.CreatePropertyView.as_view(),name='property-new',),
	)