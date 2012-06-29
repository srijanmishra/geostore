# geostore core invoke service
import kestrel.core.workflow

# input service string Service Key [kwargs] optional
# output request dict Request [kwargs] optional
def run(request, **kwargs):
	mappings = {
		'demo' : 'geostore.core.demo',
	}
	
	return kestrel.core.workflow.run(request, mappings, **kwargs)
	