from django.conf.urls import patterns, include, url
from activity_site import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'activity_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
        url(r'^login/', views.view_login),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^api/ops/', include('ops_admin.urls')),
        url(r'^api/', include('front_api.urls')),
    )
