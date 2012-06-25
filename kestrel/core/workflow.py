# kestrel core workflow service
import kestrel.core.response

# 
# input service string Service Key [kwargs] optional
# input mapping dict Service Mappings [kwargs] optional
#
# output request dict Request [kwargs] optional
#
def run(request, **kwargs):
	service = kwargs.get('service', request.REQUEST.get('service', None))
	kwargs['request'] = request
	
	if service != None:
		mappings = kwargs.get('mappings', {})
		service = mappings.get(service, service)
		try:
			service = __import__(service, globals(), locals(), ['run'], -1)
			kwargs = service.run(kwargs)
		except Exception :
			pass
	
	return kestrel.core.response.run(kwargs)
