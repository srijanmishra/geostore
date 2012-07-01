# kestrel core workflow service
from django.utils import simplejson
import kestrel.core.response

# 
# input service string Service Key [kwargs] optional
# input mapping dict Service Mappings [kwargs] optional
#
# output request dict Request [kwargs] optional
#
def run(request, mappings = {}, parse = 'post', service = None, operation = None, id = None, format = None, **kwargs):
	if parse == 'post':
		data = request.POST
	elif parse == 'get':
		data = request.GET
	elif parse == 'json':
		data = simplejson.loads(request.body)
	else:
		data = {}
	
	config = mappings.get(service, None)
	print config
	if config != None:
		#try:
			service = getattr(__import__(config[0], globals(), locals(), [operation if operation else config[1]], -1), operation if operation else config[1])
			kwargs = service(request, **(dict(kwargs.items() + data.items())))
			#service = __import__(config[0], globals(), locals(), [operation if operation else config[1]], -1)
			#kwargs = service.run(request, **(dict(kwargs.items() + data.items())))
			print kwargs
		#except Exception:	
		#	pass
	elif service:
		kwargs['page'] = service + ('/' + operation if operation else '') + ('/' + id if id else '')
	
	return kestrel.core.response.run(request, format, **kwargs)
