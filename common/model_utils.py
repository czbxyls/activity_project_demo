from django.db import models
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db.models.query import QuerySet
from django.db import connection
import json
import re
import logging

class BaseModel(models.Model):
	# to json string
	def to_jsonstring(self):
		return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

	def __str__(self):
		return self.to_jsonstring()

	class Meta:
		abstract = True


def to_json(result):
	if isinstance(result, (QuerySet, RawQuerySet)):
		ret_list = []
		for item in result:
			ret_list.append(json.loads(to_json(item)))
		return ret_list
	elif isinstance(result, BaseModel):
		return result.to_jsonstring()
	else:
		return json.dumps(result)
	#elif isinstance(result, (dict,list,str,bool,int,float,long,unicode)):
	#	return json.dumps(result)
	#return serializers.serialize('json', result)


def pagination(manager, **kwargs):
	page = 0
	size = 20
	fields = None
	ignore_field_list = ["page", "size", "fields"]
	params = {}
	if kwargs:
		page = kwargs.get("page", page)
		size = kwargs.get("size", size)
		fields = kwargs.get("order_by", fields)
		for k, v in kwargs.items():
			if k not in ignore_field_list:
				params[k] = v
	size = 20 if size <= 0 else size
	page = 0 if page < 0 else page
	left = page * size
	right = (page + 1) * size
	if fields:
		manager = manager.values(*fields)
	if params:
		ret = manager.filter(**params)[left:right]
		count = manager.filter(**params).count()
	else:
		ret = manager.all()[left:right]
		count = manager.count()
	ret_dict = {'list': to_json(ret), "page": page, "size": size, "count": count}
	return ret_dict



