import uuid


def is_empty(string):
    return not(string and string.strip())


def is_not_empty(string):
	return not(is_empty(string))


def get_uuid():
	return str(uuid.uuid1()).replace("-", "")
