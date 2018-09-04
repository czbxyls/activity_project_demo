""" auth helper for login, including some config"""
from django.core.cache import cache
from common import common_utils

"""redis auth cache timeout setting"""
COMMON_AUTH_SESSION_TIMEOUT = 10 * 60
type_sessionkey_dict = {
	0: "uid", # for front_api user
	1: "admid" # for ops_admin admin user
}


class AuthSession:
	def __init__(self, request, user_type=0):
		self.uid_key_name = type_sessionkey_dict.get(user_type, "uid")
		self.request = request

	def __get_cache_uuid_key(self, uuid_str):
		return self.uid_key_name + '_uuid_' + uuid_str

	def __get_cache_uid_key(self, uid):
		return self.uid_key_name + "_" + str(uid)

	def save(self, uid):
		# if login in other session, clear cache
		self.__remove(uid)
		uuid_str = common_utils.get_uuid()
		cache.set(self.__get_cache_uuid_key(uuid_str), uid, timeout=COMMON_AUTH_SESSION_TIMEOUT)
		cache.set(self.__get_cache_uid_key(uid), uuid_str, timeout=COMMON_AUTH_SESSION_TIMEOUT)
		return uuid_str

	def update(self, uid):
		uuid_str = self.request.COOKIES.get(self.uid_key_name, '0')
		cache.expire(self.__get_cache_uuid_key(uuid_str), timeout=COMMON_AUTH_SESSION_TIMEOUT)
		cache.expire(self.__get_cache_uid_key(uid), timeout=COMMON_AUTH_SESSION_TIMEOUT)

	def __remove(self, uid):
		uuid_str = cache.get(self.__get_cache_uid_key(uid))
		if uuid_str:
			cache.set(self.__get_cache_uuid_key(uuid_str), uid, timeout=0)
			cache.set(self.__get_cache_uid_key(uid), uuid_str, timeout=0)

	def get_uid_by_uuid(self, uuid_str):
		uid = cache.get(self.__get_cache_uuid_key(uuid_str), 0)
		return long(uid)

	def get_uuid(self, uid):
		uuid = cache.get(self.__get_cache_uid_key(uid), "")
		return uuid

	def get_uid(self):
		uuid_str = self.request.COOKIES.get(self.uid_key_name, '0')
		return self.get_uid_by_uuid(uuid_str)

	def is_login(self):
		uid = self.get_uid()
		return uid > 0


