from django.conf.urls import patterns, include, url
from ops_admin import views

urlpatterns = patterns('',
    url(r'^channel/add/$', views.view_api_ops_channel_add),
    url(r'^channel/update/$', views.view_api_ops_channel_update),
    url(r'^channel/delete/$', views.view_api_ops_channel_delete),
    url(r'^channel/query/$', views.view_api_ops_channel_query),
    url(r'^activity/add/$', views.view_api_ops_activity_add),
    url(r'^activity/update/$', views.view_api_ops_activity_update),
    url(r'^activity/delete/$', views.view_api_ops_activity_delete),
    url(r'^activity/query/$', views.view_api_ops_activity_query),
    url(r'^activity/detail/$', views.view_api_ops_activity_detail),
    url(r'^auth/login/$', views.view_api_ops_auth_login),
)

