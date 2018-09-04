from activitylib import form_schema
from common import error,  time_utils
from activity_logic import service_di
from activitylib.auth_session import AuthSession
from activitylib.decorator import exception_check,parameter_check,login_check
from common.api_utils import response_ok


# Create your views here.
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_AUTH_LOGIN_SCHEMA)
def view_api_auth_login(request):
	params = request.data
	username = params.get("username", None)
	password = params.get("password", None)
	user = service_di.userService.get(username)
	if not user or password != user.password:
		raise error.MessageError("username error or password error")
	ret = {"username": user.username, "photo_url": user.photo_url, "email": user.email}
	response = response_ok(request, ret)
	session = AuthSession(request)
	uuid_str = session.save(user.user_id)
	response.set_cookie("uid", uuid_str)
	return response


@login_check()
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_ACTIVITY_QUERY_SCHEMA)
def view_api_activity_query(request):
	params = request.data
	channel_id = long(params.get("channel_id", 0))
	begin_time = long(params.get("begin_time", 0))
	end_time = long(params.get("end_time", 0))
	page = int(params.get("page", 0))
	size = int(params.get("size", 20))
	now = time_utils.unix_time()
	fields_dict = {"page": page, "size": size}
	if channel_id > 0:
		fields_dict["a.channel_id"] = channel_id
	if begin_time > 0:
		fields_dict["end_time__gte"] = begin_time
	if end_time > 0:
		fields_dict["begin_time__lte"] = end_time
	else:
		fields_dict["end_time__gte"] = now
	fields_dict["order_by"] = "order by a.id desc"
	ret = service_di.activityService.query_summary_page(**fields_dict)
	return response_ok(request, ret)


@login_check()
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_ACTIVITY_COMMON_SCHEMA)
def view_api_activity_detail(request):
	params = request.data
	activity_id = int(params.get("activity_id", 0))
	ret = service_di.activityService.detail_summary(activity_id)
	return response_ok(request, ret)


@login_check()
#@exception_check
@parameter_check(method='ALL')
def view_api_activity_query_mine(request):
	params = request.data
	page = int(params.get("page", 0))
	size = int(params.get("size", 20))
	user_id = request.uid
	ret = service_di.activityService.query_mine_page(user_id, page, size)
	return response_ok(request, ret)


@login_check()
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_ACTIVITY_JOIN_SCHEMA)
def view_api_activity_join(request):
	params = request.data
	now = time_utils.unix_time()
	activity_id = long(params.get("activity_id", 0))
	is_join = "True" == params.get("is_join", "True")
	user_id = request.uid
	service_di.activityService.join(user_id, activity_id, is_join)
	return response_ok(request, True)


@login_check()
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_ACTIVITY_COMMENT_SCHEMA)
def view_api_activity_comment(request):
	params = request.data
	now = time_utils.unix_time()
	activity_id = long(params.get("activity_id", 0))
	refer_id = long(params.get("refer_id", 0))
	content = params.get("content", None)
	user_id = request.uid
	service_di.activityService.comment(user_id, activity_id, refer_id, content)
	return response_ok(request, True)


@login_check()
#@exception_check
@parameter_check(method='ALL', schema=form_schema.API_ACTIVITY_COMMON_SCHEMA)
def view_api_activity_query_comments(request):
	params = request.data
	activity_id = long(params.get("activity_id", 0))
	page = int(params.get("page", 0))
	size = int(params.get("size", 20))
	ret = service_di.activityService.query_comments(activity_id, page, size)
	return response_ok(request, ret)


@login_check()
@exception_check
@parameter_check(method='ALL', schema=form_schema.API_ACTIVITY_COMMON_SCHEMA)
def view_api_activity_query_participators(request):
	params = request.data
	activity_id = long(params.get("activity_id", 0))
	page = int(params.get("page", 0))
	size = int(params.get("size", 20))
	ret = service_di.activityService.query_participators(activity_id, page, size)
	return response_ok(request, ret)


@login_check()
@exception_check
@parameter_check(method='ALL')
def view_api_channel_get_all(request):
	ret = service_di.activityChannelService.get_all()
	return response_ok(request, ret)