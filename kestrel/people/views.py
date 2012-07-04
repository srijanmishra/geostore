from django.contrib.auth.models import User
from kestrel.people.models import Person
from kestrel.people.forms import RegistrationForm
from kestrel.core import response

def register(request, **kwargs):
	kwargs['page'] = 'account/login'
	success = False
	
	if request.user.is_authenticated():
		return response.run(request, **kwargs)
	
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			u = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
			u.get_profile().verify()
			success = True
	else:
		form = RegistrationForm()
	
	kwargs['data'] = { 'form' : form, 'success' : success }
	return response.run(request, **kwargs)

def verify(request, **kwargs):
	kwargs['page'] = 'account/verify'
	success = False
	
	if request.user.is_authenticated():
		return response.run(request, **kwargs)
	
	username = kwargs.pop('username', None)
	code = kwargs.pop('code', None)
	
	if username and code:
		u = User.objects.get(username = username)
		success = u.get_profile().confirm(code)
	
	kwargs['data'] = { 'success' : success }
	return response.run(request, **kwargs)
	
def profile(request, **kwargs):
	kwargs['page'] = 'page/person'
	data = { 'success' : False, 'errors' : None, 'view' : True }
	user = request.user.get_profile().id if request.user.is_authenticated() else -1
	
	if kwargs.get('username', None):
		try:
			u = User.objects.get(username = kwargs.pop('username', None))
			p = u.get_profile()
			data['success'] = True
			data['user'] = u
			data['person'] = p
			data['admin'] = p.guard(user = user, action = 'edit', iaction = 'edit', color = 'owner', icolor = 'all')
		except Exception:
			data['errors'] = 'Invalid username'
	else:
		data['errors'] = 'Invalid username'
	
	kwargs['data'] = data
	return response.run(request, **kwargs)
