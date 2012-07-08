from django.contrib.auth.models import User
from kestrel.people.models import Person

def edit(request, csrfmiddlewaretoken, username, first_name, last_name, 
	desc = '', phone = '', address = '', gender = 'N', dateofbirth = None, edit = None,  _ts = None, **kwargs):
	kwargs['page'] = 'page/person'
	data = { 'valid' : False, 'errors' : None }
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		u = User.objects.get(username = username)
		p = u.get_profile()
		u.first_name = first_name
		u.last_name = last_name
		p.desc = desc
		p.phone = phone
		p.address = address
		p.gender = gender
		if dateofbirth:
			p.dateofbirth = dateofbirth
		try: 
			p.edit(user = user)
			u.save()
			data['valid'] = True
		except: 
			data['errors'] = 'Not Authorized'
		
		data['user'] = u
		data['person'] = p
		data['admin'] = 1
	except Exception:
		data['errors'] = 'Invalid User'
		data['edit'] = not data['valid']	data['view'] = data['valid']
	kwargs['data'] = data
	return kwargs

def passwd(request, csrfmiddlewaretoken, username, current, password, cnfpasswd, passwd = None,  _ts = None, **kwargs):
	kwargs['page'] = 'page/person'
	data = { 'valid' : False, 'errors' : None, 'passwd' : True }
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		u = User.objects.get(username = username)
		p = u.get_profile()
		if request.user.check_password(current):
			if password == cnfpasswd:
				u.set_password(password)
				try:
					p.edit(user = user)
					u.save()
					data['valid'] = True
				except:
					data['errors'] = 'Not Authorized'
			else:
				data['errors'] = 'Passwords do not match'
		else:
			data['errors'] = 'Invalid Credentials'
		
		data['user'] = u
		data['person'] = p
		data['admin'] = 1
	except Exception:
		data['errors'] = 'Invalid User'
		
	kwargs['data'] = data
	return kwargs

def photo(request, csrfmiddlewaretoken, username, photo = None,  _ts = None, **kwargs):
	kwargs['page'] = 'page/person'
	data = { 'valid' : False, 'errors' : None }
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		u = User.objects.get(username = username)
		p = u.get_profile()
		p.photo.file = request.FILES['file']
		p.photo.mime = request.FILES['file'].content_type
		#try: 
		p.photo.edit(user = user)
		data['valid'] = True
	#except: 
		data['errors'] = 'Not Authorized'

		data['user'] = u
		data['person'] = p
		data['admin'] = 1
	except User.DoesNotExist:
		data['errors'] = 'Invalid User'
		data['photo'] = not data['valid']	data['view'] = data['valid']
	kwargs['data'] = data
	return kwargs

def reset(request, csrfmiddlewaretoken, username, resetpass = None, **kwargs):
	kwargs['page'] = 'account/login'
	valid = False
	errors = None
	
	if request.user.is_authenticated():
		return kwargs
	
	try:
		u = User.objects.get(username = username)
		if u.get_profile().reset():
			valid = True
		else:
			errors = 'Error Sending Mail'
	except Exception:
		errors = 'Invalid Username'
	
	kwargs['data'] = { 'valid' : valid, 'errors' : errors }
	return kwargs
