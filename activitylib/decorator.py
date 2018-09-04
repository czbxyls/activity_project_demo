#-*- coding:utf-8 -*-
import logging
from functools import wraps
from django.http import HttpResponse,HttpResponseRedirect
from activitylib import auth_session
from django.utils.decorators import available_attrs
from jsonschema import validate
from jsonschema import exceptions
from common import api_utils
from common import error
logger = logging.getLogger("activity.common")


def	login_check(user_type=0):
	def decorator(func):
		@wraps(func, assigned=available_attrs(func))
		def returned_wrapper(request, *args, **kwargs):
			auth = auth_session.AuthSession(request, user_type)
			if not auth.is_login():
				return HttpResponseRedirect('/login')
			request.uid = auth.get_uid()
			auth.update(request.uid)
			return func(request, *args, **kwargs)
		return returned_wrapper
	return decorator


def exception_check(func):
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			try:
				return view_func(request, *args, **kwargs)
			except error.MessageError as m:
				logger.error('%s: %s' % (view_func.__name__, m))
				return api_utils.response_error(request, m.message)
			except exceptions.ValidationError as v:
				return api_utils.response_error(request, v.message)
			except Exception as e:
				logger.error('%s: %s' %(view_func.__name__, e))
				return api_utils.response_error(request, u'系统繁忙, 请稍后重试')
		return _wrapped_view
	return decorator(func)


def parameter_check(method='GET', schema=None):
	def decorator(func):
		@wraps(func, assigned=available_attrs(func))
		def returned_wrapper(request, *args, **kwargs):
			request_dict = {
				"GET": request.GET,
				"POST": request.POST
			}
			query_dict = request_dict.get(method, request.REQUEST)
			data = {}
			for k, v in query_dict.items():
				data[k] = v
			request.data = data
			if schema:
				try:
					validate(data, schema)
				except exceptions.ValidationError as v:
					logger.error("data = %s, error = %s" %(data, v.message))
					raise error.MessageError("invalid parameter")
				# if schema.has_key('required'):
				# 	required_list = schema['required']
				# 	for item in required_list:
				# 		if not data.has_key(item):
				# 			raise error.MessageError(item + ' is required!')
				# if schema.has_key('properties'):
				# 	logging.error(str(schema['properties']))
				# 	for k, check_schema in schema['properties'].items():
				# 		form_schema.schema_check(k, check_schema, data.get(k))
			return func(request, *args, **kwargs)
		return returned_wrapper
	return decorator