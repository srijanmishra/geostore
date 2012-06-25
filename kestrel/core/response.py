# kestrel core response service
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

def run(kwargs):
	if kwargs.has_key('page') and kwargs.get('page') == None:
		del kwargs['page']
	
	if kwargs.get('format', 'html') == 'json':
		return HttpResponse(
			simplejson.dumps(kwargs.get('data', {})), 
			mimetype='application/json'
		)
	else:
		return render_to_response(
			kwargs.get('page', 'page/home') + '.html', 
			kwargs.get('data', {}), 
			context_instance = RequestContext(kwargs.get('request', None))
		)
