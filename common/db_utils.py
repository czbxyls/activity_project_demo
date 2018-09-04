from django.db import connection
import re


def __get_sql_fields(sql_by_where, *args):
	params_list = [arg for arg in args]
	return (sql_by_where, params_list)


def query(sql_by_where, *args):
	sql_fields = __get_sql_fields(sql_by_where, *args)
	cursor = connection.cursor()
	try:
		cursor.execute(sql_fields[0], sql_fields[1])
		desc = cursor.description
		ret_list = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
		return ret_list
	finally:
		cursor.close()


def query_value(sql_by_where, *args):
	sql_fields = __get_sql_fields(sql_by_where, *args)
	cursor = connection.cursor()
	try:
		cursor.execute(sql_fields[0], sql_fields[1])
		desc = cursor.description
		ret_list = [row[0] for row in cursor.fetchall()]
		return ret_list
	finally:
		cursor.close()


def find(sql_by_where, *args):
	sql_fields = __get_sql_fields(sql_by_where, *args)
	cursor = connection.cursor()
	try:
		cursor.execute(sql_fields[0], sql_fields[1])
		desc = cursor.description
		ret_dict = dict(zip([col[0] for col in desc], cursor.fetchone()))
		return ret_dict
	finally:
		cursor.close()


def find_value(sql_by_where, *args):
	sql_fields = __get_sql_fields(sql_by_where, *args)
	cursor = connection.cursor()
	try:
		cursor.execute(sql_fields[0], sql_fields[1])
		ret = cursor.fetchone()
		return ret[0] if ret and len(ret) > 0 else None
	finally:
		cursor.close()


def query_pagination(sql_with_where, param_list, page, size):
	size = 20 if size <= 0 else size
	page = 0 if page < 0 else page
	left = page * size
	new_sql = re.sub(r'^(select|SELECT)', "SELECT SQL_CALC_FOUND_ROWS", sql_with_where.lstrip(), 1)
	new_sql = "%s limit %d, %d" %(new_sql, left, size)
	ret_list = query(new_sql, *param_list)
	count = find_value("SELECT FOUND_ROWS()")
	ret_dict = {'list': ret_list, "page": page, "size": size, "count": count}
	return ret_dict


def query_pagination2(sql, **kwargs):
	page = 0
	size = 20
	new_sql = sql
	params_list = []
	ignore_field_list = ["page", "size", "order_by"]
	if kwargs:
		page = kwargs.get("page", page)
		size = kwargs.get("size", size)
		order_by = kwargs.get("order_by", None)
		for k, v in kwargs.items():
			if k in ignore_field_list:
				continue
			new_sql += " and " + __parse_query_fileds_name(k, v)
			params_list.append(v)
		if order_by:
			new_sql += " " + order_by
	return query_pagination(new_sql, params_list, page, size)


def __parse_query_fileds_name(field_name, filed_value):
	inline_keys = {
		"__gt": lambda v: ">%s",
		"__gte": lambda v: ">=%s",
		"__lt": lambda v: "<%s",
		"__lte": lambda v: "<=%s",
	}
	match = False
	for k, func in inline_keys.items():
		if field_name.endswith(k):
			field_name = field_name.replace(k, func(filed_value))
			match = True
			break
	if not match:
		field_name += "=%s"
	field_name = field_name.replace("__", ".", 1)
	return field_name
