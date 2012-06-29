# orbitnote core demo service

def run(request, kwargs):
	kwargs['data'] = {
		'text' : 'OrbitNote Demo'
	}
	
	kwargs['page'] = 'page/demo'
	return kwargs
