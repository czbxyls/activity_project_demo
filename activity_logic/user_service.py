from common import time_utils, model_utils
from activitylib import models, cache_key_def
from django.core.cache import cache
import json
from activitylib.cache_key_def import VIEWS_CACHE_DATA_TTL


class UserService:
	def __init__(self):
		pass

	def get(self, username):
		return models.User.objects.filter(username=username).get()

	def get_user_dict(self, user_idlist):
		user_list =  models.User.objects\
			.extra(select={'user_id': 'user_id', 'username': 'username', 'photo_url': 'photo_url'})\
			.filter(user_id__in=user_idlist).values('user_id', 'username', 'photo_url')
		ret_dict = {}
		for user in user_list:
			ret_dict[user["user_id"]] = user
		return ret_dict


class AdminService:

	def __init__(self):
		self.admin_dict = {}
		self.last_uptime = time_utils.unix_time()
		pass

	def get_name(self, id):
		now = time_utils.unix_time()
		if not self.admin_dict or now - self.last_uptime >= 1:
			redis_admin_dict_str = cache.get(cache_key_def.REDIS_KEY_API_ADMIN_DICT)
			if not redis_admin_dict_str:
				self.admin_dict = self._sync_admin_from_db()
			else:
				redis_admin_dict = json.loads(redis_admin_dict_str)
				for k, v in redis_admin_dict.items():
					self.admin_dict[long(k)] = v
		return self.admin_dict.get(id)

	def _sync_admin_from_db(self):
		admin_dict = {}
		admin_list = models.Admin.objects.all()
		for admin in admin_list:
			admin_dict[admin.admin_id] = admin.username
		cache.set(cache_key_def.REDIS_KEY_API_ADMIN_DICT, model_utils.to_json(admin_dict), VIEWS_CACHE_DATA_TTL)
		return admin_dict

	def get(self, username):
		return models.Admin.objects.filter(username=username).get()
