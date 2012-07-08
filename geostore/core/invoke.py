# geostore core invoke service
import kestrel.core.workflow

mappings = {
	'demo' : ('geostore.core.demo', 'run'),
	'user' : ('kestrel.people.person', 'edit'),
	'storage' : ('kestrel.storage.services', 'list'),
}

def run(request, **kwargs):
	print kwargs
	return kestrel.core.workflow.run(request, mappings, None, **kwargs)

def post(request, **kwargs):
	print kwargs
	return kestrel.core.workflow.run(request, mappings, 'post', **kwargs)

def json(request, **kwargs):
	print kwargs
	return kestrel.core.workflow.run(request, mappings, 'json', **kwargs)
