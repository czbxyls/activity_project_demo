from django.http import HttpResponse
from django.template import loader,Context


def view_login(request):
	t = loader.get_template("login.html")
	c = Context({})
	return HttpResponse(t.render(c))