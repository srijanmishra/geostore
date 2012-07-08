from django.conf import settings
from django.contrib.auth.models import User
# from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.http import Http404
from kestrel.storage.models import Directory, File
from kestrel.core import utils

def list(request, username, id = settings.STORAGE_BUCKET_ID, **kwargs):
	kwargs['page'] = 'page/storage'
	data = { 'list' : True }
	
	if not utils.is_numeric(id): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	data['regions'] = settings.STORAGE_NAMES if float(id) == settings.STORAGE_BUCKET_ID else False
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		d = Directory.objects.get(id = id)
		u = User.objects.get(username = username)
		p = u.get_profile()
		
		try: 
			ds = d.list(user = user, type = 'directory', lcolor = username)
			data['directories'] = ds
			fs = d.list(user = user, type = 'file', lcolor = username)
			data['files'] = fs
			data['valid'] = True
		except: 
			data['errors'] = 'Not Authorized'

		data['user'] = u
		data['person'] = p
		data['storage'] = d
		data['admin'] = p.guard(user = user, action = 'add')
	except Directory.DoesNotExist:
		data['errors'] = 'Invalid Storage'
	
	kwargs['data'] = data
	return kwargs

def add(request, username, name, root = 0, id = settings.STORAGE_BUCKET_ID, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	kwargs['page'] = 'storage/directory'
	data = { 'view' : True }
	
	if not utils.is_numeric(id, root): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	data['regions'] = settings.STORAGE_NAMES if float(id) == settings.STORAGE_BUCKET_ID else False
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		s = Directory.objects.get(id = id)
		p = request.user.get_profile() if request.user.is_authenticated() else None
		
		name = get_available_name(name, s, user, request)
		try:
			d = Directory(name = name, type = 'directory',  parent = s, owner = p, author = request.user.username)
			if data['regions']:
				d.root = int(root)
			d.add(user = user, ecolor = 'all.' + request.user.username)
			data['directory'] = d
		except utils.GuardException: 
			return utils.fail(kwargs, data = data, errors = 'Not Authorized')
			
		data['storage'] = s
		data['admin'] = p.guard(user = user, action = 'add')
	except Directory.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid Storage')
	
	return utils.success(kwargs, data = data)

def rename(request, username, name, id, parent = settings.STORAGE_BUCKET_ID, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	kwargs['page'] = 'storage/directory'
	data = { 'view' : True }
	
	if not utils.is_numeric(id): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	#if(float(parent) == settings.STORAGE_BUCKET_ID): return utils.fail(kwargs, data = data, errors = 'Objects are not allowed here.')
	
	data['regions'] = settings.STORAGE_NAMES if float(parent) == settings.STORAGE_BUCKET_ID else False
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		s = Directory.objects.get(id = parent)
		p = request.user.get_profile() if request.user.is_authenticated() else None
		
		d = Directory.objects.get(id = id)
		data['directory'] = d
		
		try:
			if d.name != name:
				name = get_available_name(name, s, user, request)
				d.edit(user = user)
				d.rename(name)
		except utils.GuardException: 
			return utils.fail(kwargs, data = data, errors = 'Not Authorized')

		data['storage'] = s
		data['admin'] = p.guard(user = user, action = 'add')
	except Directory.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid Storage')
	
	return utils.success(kwargs, data = data)

def rmdir(request, id, parent = settings.STORAGE_BUCKET_ID, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	kwargs['page'] = 'storage/directory'
	data = { 'view' : True }
	
	if not utils.is_numeric(id): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	#if(float(parent) == settings.STORAGE_BUCKET_ID): return utils.fail(kwargs, data = data, errors = 'Objects are not allowed here.')
	
	data['regions'] = settings.STORAGE_NAMES if float(parent) == settings.STORAGE_BUCKET_ID else False
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		s = Directory.objects.get(id = parent)
		p = request.user.get_profile() if request.user.is_authenticated() else None
		
		d = Directory.objects.get(id = id)
		data['directory'] = d
		
		try:
			d.remove(user = user)
		except utils.GuardException: 
			return utils.fail(kwargs, data = data, errors = 'Not Authorized')

		data['storage'] = s
		data['admin'] = p.guard(user = user, action = 'add')
	except Directory.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid Storage')
	
	return utils.success(kwargs, data = data)

def file(request, id, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	try:
		f = File.objects.get(id = id)
		f.info(user = user)
		path = f.get_path()
		# wrapper = FileWrapper(open( path, "r" ))
		response = HttpResponse(content_type = f.mime)
		response['Content-Length'] = f.file.size
		response['Content-Disposition'] = 'attachment; filename=%s' % f.name
		response.write(open(path, "rb").read())
		return response
	except File.DoesNotExist:
		raise Http404
	except utils.GuardException: 
		raise Http404

def upload(request, username, name = None, id = None, parent = settings.STORAGE_BUCKET_ID, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	kwargs['page'] = 'storage/file'
	data = { 'view' : True }
	
	if (id and not utils.is_numeric(id)) or (not name and not request.FILES): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	if(float(parent) == settings.STORAGE_BUCKET_ID):
		return utils.fail(kwargs, data = data, errors = 'Objects are not allowed here.')
	
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		s = Directory.objects.get(id = parent)
		p = request.user.get_profile() if request.user.is_authenticated() else None
		name = name if name else request.FILES['file'].name
		
		if not id:
			name = get_available_name(name, s, user, request)
			try:
				f = File(name = name, type = 'file',  parent = s, owner = p, author = request.user.username)
				print f.id
				f.add(user = user, ecolor = 'all.' + request.user.username)
				data['file'] = f
			except utils.GuardException: 
				return utils.fail(kwargs, data = data, errors = 'Not Authorized')
		else:
			f = File.objects.get(id = id)
			data['file'] = f
		
		if request.FILES:
			try:
				f.file = request.FILES['file']
				f.mime = request.FILES['file'].content_type
				f.edit(user = user)
			except utils.GuardException: 
				return utils.fail(kwargs, data = data, errors = 'Not Authorized')

		data['storage'] = s
		data['admin'] = p.guard(user = user, action = 'add')
	except Directory.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid Storage')
	
	return utils.success(kwargs, data = data)

def change(request, username, name = None, id = None, parent = settings.STORAGE_BUCKET_ID, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	kwargs['page'] = 'storage/file'
	data = { 'view' : True }
	
	if not utils.is_numeric(id) or (not name and not request.FILES): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	if(float(parent) == settings.STORAGE_BUCKET_ID):
		return utils.fail(kwargs, data = data, errors = 'Objects are not allowed here.')
	
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		s = Directory.objects.get(id = parent)
		p = request.user.get_profile() if request.user.is_authenticated() else None
		name = name if name else request.FILES['file'].name
		
		f = File.objects.get(id = id)
		data['file'] = f
		
		try:
			if f.name != name:
				name = get_available_name(name, s, user, request)
				f.edit(user = user)
				f.rename(name)
			if request.FILES:
				f.file = request.FILES['file']
				f.mime = request.FILES['file'].content_type
				f.edit(user = user)
		except utils.GuardException: 
			return utils.fail(kwargs, data = data, errors = 'Not Authorized')

		data['storage'] = s
		data['admin'] = p.guard(user = user, action = 'add')
	except File.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid File')
	except Directory.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid Storage')
	
	return utils.success(kwargs, data = data)

def remove(request, id, parent = settings.STORAGE_BUCKET_ID, _ts = None, csrfmiddlewaretoken = None, **kwargs):
	kwargs['page'] = 'storage/file'
	data = { 'view' : True }
	
	if not utils.is_numeric(id): 
		return utils.fail(kwargs, data = data, errors = 'Invalid Request')
	
	if(float(parent) == settings.STORAGE_BUCKET_ID):
		return utils.fail(kwargs, data = data, errors = 'Objects are not allowed here.')
	
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	try :
		s = Directory.objects.get(id = parent)
		p = request.user.get_profile() if request.user.is_authenticated() else None
		
		f = File.objects.get(id = id)
		data['file'] = f
		
		try:
			f.remove(user = user)
		except utils.GuardException: 
			return utils.fail(kwargs, data = data, errors = 'Not Authorized')

		data['storage'] = s
		data['admin'] = p.guard(user = user, action = 'add')
	except File.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid File')
	except Directory.DoesNotExist:
		return utils.fail(kwargs, data = data, errors = 'Invalid Storage')
	
	return utils.success(kwargs, data = data)

def get_available_name(name, s, user, request):
	i = 1
	names = name.split('.')
	cname = names[0]
	while True:
		try : d = Directory.objects.get(name = name, root = s.root, id__in = s.list(user = user, type = 'directory', lcolor = request.user.username).values_list('id'))
		except Directory.DoesNotExist:
			try : f = File.objects.get(name = name, id__in = s.list(user = user, type = 'file', lcolor = request.user.username).values_list('id'))
			except File.DoesNotExist: 
				break
			else: 
				names[0] = cname + '_' + str(i)
		else: 
			names[0] = cname + '_' + str(i)
		i = i + 1
		name = '.'.join(names)
	return name
