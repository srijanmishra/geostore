# kestrel core response service
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

def run(kwargs):
	if kwargs.has_key('page') and kwargs.get('page') == None:
		del kwargs['page']
	
	# respond json data
	if kwargs.get('format', None) == 'json':
		return HttpResponse(
			simplejson.dumps(kwargs.get('data', {})), 
			mimetype='application/json'
		)
	# respond kestrel base html
	elif kwargs.get('format', None) == 'html':
		data = kwargs.get('data', {})
		data['kestrel'] = 'html'
		return render_to_response(
			kwargs.get('page', 'page/home') + '.html', 
			data, 
			context_instance = RequestContext(kwargs.get('request', None))
		)
	# respond base html
	else:
		return render_to_response(
			kwargs.get('page', 'page/home') + '.html', 
			kwargs.get('data', {}), 
			context_instance = RequestContext(kwargs.get('request', None))
		)
