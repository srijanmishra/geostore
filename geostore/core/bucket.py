from kestrel.storage.models import Directory

def list(request, username, **kwargs):
	kwargs['page'] = 'page/buckets'
	data = { 'valid' : False, 'errors' : None, 'list' : True }
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		u = User.objects.get(username = username)
		p = u.get_profile()
		
		try: 
			bs = p.list(user = user, type = 'bucket')
			data['valid'] = True
		except: 
			data['errors'] = 'Not Authorized'

		data['user'] = u
		data['person'] = p
		data['buckets'] = bs
		data['admin'] = p.guard(user = user, action = 'add', iaction = 'add')
	except Exception:
		data['errors'] = 'Invalid User'
	
	kwargs['data'] = data
	return kwargs
