# geostore core invoke service
import kestrel.core.workflow

mappings = {
	'demo' : ('geostore.core.demo', 'run'),
	'user' : ('kestrel.people.views', 'profile'),
}

# input service string Service Key [kwargs] optional
# output request dict Request [kwargs] optional
def run(request, **kwargs):
	return kestrel.core.workflow.run(request, mappings, None, **kwargs)

def post(request, **kwargs):
	return kestrel.core.workflow.run(request, mappings, 'post', **kwargs)
