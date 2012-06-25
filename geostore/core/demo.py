# orbitnote core demo service

def run(kwargs):
	kwargs['data'] = {
		'text' : 'OrbitNote Demo'
	}
	
	kwargs['page'] = 'page/demo'
	return kwargs
