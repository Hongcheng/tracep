from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template,Context

def Home_Page(request):
	t = get_template('home_page.html')
	html = t.render(Context())
	return HttpResponse(html)