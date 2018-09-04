class MessageError(Exception):
	"""
		A class for show message exception
	"""
	def __init__(self, message, code):
		self.message = message
		self.code = code

	def __init__(self, message):
		self.message = message
		self.code = 0

	def __str__(self):
		return 'message=%s, code=%d' %(repr(self.message), self.code)