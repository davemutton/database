from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls.static import static
from property import views



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'database.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^property/', include('property.urls')),
    url(r'^api/', include('api.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)












'''from django.conf.urls import patterns, include, url
from django.conf import settingsbclass GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'database.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^property/', include('property.urls')),
 
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''