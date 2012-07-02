# geostore core invoke service
import kestrel.core.workflow

mappings = {
	'demo' : ('geostore.core.demo', 'run'),
	'user' : ('kestrel.people.services', 'profile'),
}

def run(request, **kwargs):
	return kestrel.core.workflow.run(request, mappings, None, **kwargs)

def post(request, **kwargs):
	return kestrel.core.workflow.run(request, mappings, 'post', **kwargs)

def json(request, **kwargs):
	return kestrel.core.workflow.run(request, mappings, 'json', **kwargs)
