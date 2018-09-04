from common import time_utils
from common import model_utils
from django.core import serializers
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponse
import json

"""api utils for response of json data"""

def response_ok(request, data):
	return HttpResponse(ApiResponse().ok(data).to_json(), content_type='application/json; charset=utf-8')


def response_error(request, desc):
	return HttpResponse(ApiResponse().error(desc).to_json(), content_type='application/json; charset=utf-8')


class ApiResponse:
	def __init__(self):
		self.status = 200
		self.subtime = 0

	def ok(self, data):
		self.status = 200
		self.subtime = time_utils.unix_time()
		self.result = data
		return self

	def error(self, desc):
		self.status = 500
		self.subtime = time_utils.unix_time()
		self.error = desc
		return self

	def to_json(self):
		return json.dumps(self, default=to_serializable)


def to_serializable(obj):
	ret_dict = {}
	for attr in obj.__dict__:
		value = getattr(obj, attr)
		if value is not None:
			ret_dict[attr] = value
	return ret_dict
