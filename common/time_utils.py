from datetime import datetime
import time


def unix_time():
	return int(time.time())


def now():
	return datetime.now()