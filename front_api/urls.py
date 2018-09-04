from django.conf.urls import patterns, include, url
from front_api import views

urlpatterns = patterns('',
    url(r'^activity/query/$', views.view_api_activity_query),
    url(r'^activity/detail/$', views.view_api_activity_detail),
	url(r'^activity/query_mine/$', views.view_api_activity_query_mine),
	url(r'^activity/join/$', views.view_api_activity_join),
	url(r'^activity/comment/$', views.view_api_activity_comment),
	url(r'^activity/query_comments/$', views.view_api_activity_query_comments),
	url(r'^activity/query_participators/$', views.view_api_activity_query_participators),
	url(r'^channel/get_all/$', views.view_api_channel_get_all),
	url(r'^auth/login/$', views.view_api_auth_login),
)

