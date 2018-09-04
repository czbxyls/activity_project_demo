#-*- coding:utf-8 -*-
from activitylib import form_schema
from activitylib.decorator import exception_check,parameter_check,login_check
from common import common_utils
from common import error
from common import time_utils
from activity_logic import service_di
from activitylib.auth_session import AuthSession
from common.api_utils import response_ok

# Create your views here.


@exception_check
@parameter_check(method='ALL', schema=form_schema.API_AUTH_LOGIN_SCHEMA)
def view_api_ops_auth_login(request):
	params = request.data
	username = params.get("username", None)
	password = params.get("password", None)
	admin = service_di.adminService.get(username)
	if not admin or password != admin.password:
		raise error.MessageError("username error or password error")
	ret = {"username": admin.username}
	response = response_ok(request, ret)
	session = AuthSession(request, 1)
	uuid_str = session.save(admin.admin_id)
	response.set_cookie("admid", uuid_str)
	return response


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_OPS_CHANNEL_ADD_SCHEMA)
def view_api_ops_channel_add(request):
	params = request.data
	now = time_utils.unix_time()
	admin_id = request.uid
	params["create_time"] = now
	params["update_time"] = now
	params["admin_id"] = admin_id
	if id in params: params.pop("id")
	service_di.activityChannelService.create(**params)
	return response_ok(request, True)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_OPS_CHANNEL_DEL_SCHEMA)
def view_api_ops_channel_delete(request):
	params = request.data
	id = params.get("id", None)
	service_di.activityChannelService.delete(id)
	return response_ok(request, True)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_OPS_CHANNEL_UPDATE_SCHEMA)
def view_api_ops_channel_update(request):
	params = request.data
	now = time_utils.unix_time()
	admin_id = request.uid
	params["update_time"] = now
	params["admin_id"] = admin_id
	channel_id = params["id"]
	params.pop("id")
	service_di.activityChannelService.update(channel_id, **params)
	return response_ok(request, True)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL')
def view_api_ops_channel_query(request):
	params = request.data
	name = params.get("name", None)
	page = int(params.get("page", 0))
	size = int(params.get("size", 20))
	params = {}
	if common_utils.is_not_empty(name):
		params = {"name__contains": name}
	params["page"] = page
	params["size"] = size
	ret_dict = service_di.activityChannelService.query_page(**params)
	return response_ok(request, ret_dict)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_OPS_ACTIVITY_ADD_SCHEMA)
def view_api_ops_activity_add(request):
	params = request.data
	now = time_utils.unix_time()
	admin_id = request.uid
	params["create_time"] = now
	params["update_time"] = now
	params["admin_id"] = admin_id
	end_time = long(params["end_time"])
	if end_time < now:
		raise error.MessageError("end_time can not less than current time")
	if id in params:params.pop("id")
	service_di.activityService.create(**params)
	return response_ok(request, True)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_OPS_ACTIVITY_DEL_SCHEMA)
def view_api_ops_activity_delete(request):
	params = request.data
	id = params.get("id", 0)
	service_di.activityService.delete(id)
	return response_ok(request, True)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_OPS_ACTIVITY_UPDATE_SCHEMA)
def view_api_ops_activity_update(request):
	params = request.data
	now = time_utils.unix_time()
	admin_id = request.uid
	params["update_time"] = now
	params["admin_id"] = admin_id
	id = params["id"]
	params.pop("id")
	end_time = long(params["end_time"])
	if end_time < now:
		raise error.MessageError("end_time can not less than current time")
	service_di.activityService.update(id, **params)
	return response_ok(request, True)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL')
def view_api_ops_activity_query(request):
	params = request.data
	name = params.get("name", None)
	channel_id = long(params.get("channel_id", 0))
	begin_time = long(params.get("begin_time", 0))
	end_time = long(params.get("end_time", 0))
	page = int(params.get("page", 0))
	size = int(params.get("size", 20))
	params = {}
	if common_utils.is_not_empty(name):
		params["name__contains"] = name
	if channel_id > 0:
		params["channel_id"] = channel_id
	if begin_time > 0:
		params["begin_time__gte"] = begin_time
	if end_time > 0:
		params["end_time__lte"] = end_time
	fields = ("id","name","desc","location","begin_time","end_time")
	params["page"] = page
	params["size"] = size
	params["fields"] = fields
	ret_dict = service_di.activityService.query_page(**params)
	return response_ok(request, ret_dict)


@login_check(user_type=1)
@exception_check
@parameter_check(method='ALL')
def view_api_ops_activity_detail(request):
	params = request.data
	id = params.get("id", 0)
	ret_dict = service_di.activityService.detail(id)
	return response_ok(request, ret_dict)