from activitylib import models, api_sql_def, cache_key_def
from common import model_utils, time_utils
from common import error
from common import db_utils
import json
from django.core.cache import cache
import service_di
from activitylib.cache_key_def import VIEWS_CACHE_DATA_TTL


class ActivityChannelService:
	def __init__(self):
		self.channel_dict = {}
		self.last_uptime = time_utils.unix_time()
		pass

	def get_name(self, id):
		now = time_utils.unix_time()
		if not self.channel_dict or now - self.last_uptime >= 60:
			redis_channel_dict_str = cache.get(cache_key_def.REDIS_KEY_API_CHANNEL_DICT)
			if not redis_channel_dict_str:
				self.channel_dict = self._sync_channel_from_db()
			else:
				redis_channel_dict = json.loads(redis_channel_dict_str)
				for k, v in redis_channel_dict.items():
					self.channel_dict[long(k)] = v
		return self.channel_dict.get(id)

	def _sync_channel_from_db(self):
		channel_dict = {}
		channel_list = models.ActivityChannel.objects.all()
		for channel in channel_list:
			channel_dict[channel.id] = channel.name
		cache.set(cache_key_def.REDIS_KEY_API_CHANNEL_DICT, model_utils.to_json(channel_dict), VIEWS_CACHE_DATA_TTL)
		return channel_dict

	def create(self, **kwargs):
		name = kwargs.get("name")
		if models.ActivityChannel.objects.filter(name=name).count() > 0:
			raise error.MessageError("channel name duplicated")
		cache.expire(cache_key_def.REDIS_KEY_API_CHANNEL_GET_ALL, timeout=0)
		cache.expire(cache_key_def.REDIS_KEY_API_CHANNEL_DICT, timeout=0)
		ret = models.ActivityChannel.objects.create(**kwargs)
		return ret

	def delete(self, id):
		if models.Activity.objects.filter(channel_id=id).count() > 0:
			raise error.MessageError("this channel is configured in the activities, can't deleted directly")
		cache.expire(cache_key_def.REDIS_KEY_API_CHANNEL_GET_ALL, timeout=0)
		cache.expire(cache_key_def.REDIS_KEY_API_CHANNEL_DICT, timeout=0)
		ret = models.ActivityChannel.objects.filter(id=id).delete()
		return ret

	def update(self, id, **kwargs):
		cache.expire(cache_key_def.REDIS_KEY_API_CHANNEL_GET_ALL, timeout=0)
		cache.expire(cache_key_def.REDIS_KEY_API_CHANNEL_DICT, timeout=0)
		ret = models.ActivityChannel.objects.filter(id=id).update(**kwargs)
		return ret

	def query_page(self, **kwargs):
		ret_dict = model_utils.pagination(models.ActivityChannel.objects, **kwargs)
		return ret_dict

	def get_all(self):
		key = cache_key_def.REDIS_KEY_API_CHANNEL_GET_ALL
		redis_ret = cache.get(key)
		if not redis_ret:
			ret = models.ActivityChannel.objects.extra(select={'channel_id': 'id', 'channel_name': 'name'}).values(
				"channel_id", "channel_name")
			ret = model_utils.to_json(ret)
			cache.set(key, ret, VIEWS_CACHE_DATA_TTL)
		else:
			ret = redis_ret
		return ret


class ActivityService:
	def __init__(self):
		pass

	def create(self, **kwargs):
		channel_id = int(kwargs.get("channel_id", "0"))
		if models.ActivityChannel.objects.filter(id=channel_id).count() <= 0:
			raise error.MessageError("channel_id invalid")
		return models.Activity.objects.create(**kwargs)

	def delete(self, id):
		if models.Participate.objects.filter(activity_id=id).count() > 0:
			raise error.MessageError("this activity has participators, can't deleted directly")
		if models.Comment.objects.filter(activity_id=id).count() > 0:
			raise error.MessageError("this activity has comments, can't deleted directly")
		cache.expire(cache_key_def.REDIS_KEY_API_ACITITY_DETAIL_ID % (id), timeout=0)
		return models.Activity.objects.filter(id=id).delete()

	def update(self, id, **kwargs):
		channel_id = int(kwargs.get("channel_id", "0"))
		if models.ActivityChannel.objects.filter(id=channel_id).count() <= 0:
			raise error.MessageError("channel_id invalid")
		cache.expire(cache_key_def.REDIS_KEY_API_ACITITY_DETAIL_ID % (id), timeout=0)
		return models.Activity.objects.filter(id=id).update(**kwargs)

	def query_page(self, **kwargs):
		ret_dict = model_utils.pagination(models.Activity.objects, **kwargs)
		return ret_dict

	def detail(self, id):
		detail = models.Activity.objects.filter(id=id).first()
		plist = models.ActivityPicture.objects.filter(activity_id=id)
		ret_dict = json.loads(model_utils.to_json(detail))
		ret_dict["picture_list"] = model_utils.to_json(plist)
		return ret_dict

	def get_activity_dict(self, activity_idlist):
		activity_list =  models.Activity.objects\
			.extra(select={'activity_id': 'id', 'activity_name': 'name', 'activity_desc': '`desc`',
						'location': 'location', 'begin_time': 'begin_time', 'end_time': 'end_time'})\
			.filter(id__in=activity_idlist).values('activity_id', 'activity_name',
												   'activity_desc','location',
												   'begin_time', 'end_time')
		ret_dict = {}
		for activity in activity_list:
			ret_dict[activity["activity_id"]] = activity
		return ret_dict

	def query_summary_page(self, **kwargs):
		ret = db_utils.query_pagination2(api_sql_def.API_ACTIVITY_QUERY_SQL, **kwargs)
		activity_list = ret.get("list")
		for activity_dict in activity_list:
			channel_id = activity_dict.get("channel_id", 0)
			post_admin = activity_dict.get("post_admin_id", 0)
			activity_dict["channel_name"] = service_di.activityChannelService.get_name(channel_id)
			activity_dict["post_admin"] = service_di.adminService.get_name(post_admin)
		return ret

	def query_mine_page(self, user_id, page, size):
		ret = db_utils.query_pagination(api_sql_def.API_ACTIVITY_QUERY_MINE_SQL,[user_id], page, size)
		activity_idlist = []
		activity_list = ret.get("list")
		for activity_dict in activity_list:
			activity_id = activity_dict.get("activity_id", 0)
			activity_idlist.append(activity_id)
		activities = self.get_activity_dict(activity_idlist)
		for activity_dict in activity_list:
			activity_id = activity_dict.get("activity_id", 0)
			activity_dict["activity_name"] = activities.get(activity_id).get("activity_name", None)
			activity_dict["photo_url"] = activities.get(activity_id).get("photo_url", None)
			activity_dict["location"] = activities.get(activity_id).get("location", None)
			activity_dict["activity_desc"] = activities.get(activity_id).get("activity_desc", None)
			activity_dict["begin_time"] = activities.get(activity_id).get("begin_time", 0)
			activity_dict["end_time"] = activities.get(activity_id).get("end_time", 0)
		return ret

	def detail_summary(self, activity_id):
		key = cache_key_def.REDIS_KEY_API_ACITITY_DETAIL_ID % (activity_id)
		redis_ret = cache.get(key)
		if not redis_ret:
			ret = db_utils.find(api_sql_def.API_ACTIVITY_DETAIL_SQL, activity_id)
			channel_id = ret.get("channel_id", 0)
			post_admin = ret.get("post_admin_id", 0)
			ret["channel_name"] = service_di.activityChannelService.get_name(channel_id)
			ret["post_admin"] = service_di.adminService.get_name(post_admin)
			plist = models.ActivityPicture.objects.filter(activity_id=activity_id)
			ret["picture_list"] = model_utils.to_json(plist)
			cache.set(key, model_utils.to_json(ret))
		else:
			ret = redis_ret
		return ret

	def query_participators(self, activity_id, page, size):
		ret = db_utils.query_pagination(api_sql_def.API_ACTIVITY_QUERY_PARTICIPATORS_SQL, [activity_id], page, size)
		user_idlist = []
		participator_list = ret.get("list")
		for participator_dict in participator_list:
			user_id = participator_dict.get("user_id", 0)
			user_idlist.append(user_id)
		users = service_di.userService.get_user_dict(user_idlist)
		for participator_dict in participator_list:
			user_id = participator_dict.get("user_id", 0)
			participator_dict["username"] = users.get(user_id).get("username", None)
			participator_dict["photo_url"] = users.get(user_id).get("photo_url", None)
		return ret

	def query_comments(self, activity_id, page, size):
		ret = db_utils.query_pagination(api_sql_def.API_ACTIVITY_QUERY_COMMENTS_SQL, [activity_id], page, size)
		user_idlist = []
		comment_list = ret.get("list")
		for comment_dict in comment_list:
			user_id = comment_dict.get("user_id", 0)
			user_idlist.append(user_id)
		users = service_di.userService.get_user_dict(user_idlist)
		for comment_dict in comment_list:
			user_id = comment_dict.get("user_id", 0)
			comment_dict["username"] = users.get(user_id).get("username", None)
			comment_dict["photo_url"] = users.get(user_id).get("photo_url", None)
		return ret

	def comment(self, user_id, activity_id, refer_id, content):
		now = time_utils.unix_time()
		if models.Activity.objects.filter(id=activity_id).count() <= 0:
			raise error.MessageError("activity_id invalid")
		return models.Comment.objects.create(user_id=user_id, activity_id=activity_id,
									  refer_id=refer_id, content=content,
									  comment_time=now)

	def join(self, user_id, activity_id, is_join):
		now = time_utils.unix_time()
		if models.Activity.objects.filter(id=activity_id).count() <= 0:
			raise error.MessageError("activity_id invalid")
		if models.Participate.objects.filter(user_id=user_id, activity_id=activity_id).count() > 0:
			models.Participate.objects.filter(user_id=user_id, activity_id=activity_id).update(is_join=is_join,
											update_time=now)
		else:
			models.Participate.objects.create(user_id=user_id, activity_id=activity_id, is_join=True,
											create_time=now, update_time=now)


