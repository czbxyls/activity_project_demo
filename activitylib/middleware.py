import logging

logger = logging.getLogger("activity.common")


class ExceptionMiddleware(object):
	"""exception process for view"""
	def process_view(self, request, view_func, view_args, view_kwargs):
		result = view_func(request, *view_args, **view_kwargs)
		return result

	def process_request(self, request):
		return None

	def process_response(self, request, response):
		return response

	def process_exception(self, request, exception):
		pass