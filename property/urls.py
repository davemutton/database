from django.conf.urls import patterns, url
from property import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^listing/$', views.listing, name='list'),
	url(r'propertydownload/$',views.property_download, name='download'),
	url(r'^new$', views.CreatePropertyView.as_view(),name='property-new',),
	url(r'^edit/(?P<pk>\d+)/$', views.UpdatePropertyView.as_view(), name='property-edit',),
	#pages relates to displaying queries
	url(r'^query/$', views.queryjoblist, name='queryjoblist'),
	url(r'^query/(\d+)/$', views.propertyquerylist, name='propertyquerylist',),
	url(r'query/(\d+)/download/$',views.query_download, name='query_download',),
	url(r'^query/new$', views.CreateQueryJobView,name='query-new',),

	)