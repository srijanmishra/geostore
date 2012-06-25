# orbitnote core invoke service
import kestrel.core.workflow

# input service string Service Key [kwargs] optional
# output request dict Request [kwargs] optional
def run(request, **kwargs):
	kwargs['mappings'] = {
		'demo' : 'orbitnote.core.demo',
	}
	
	return kestrel.core.workflow.run(request, **kwargs)
	