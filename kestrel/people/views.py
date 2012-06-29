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
	
def reset(request, **kwargs):
	kwargs['page'] = 'account/login'
	success = False
	errors = None
	
	if request.user.is_authenticated():
		return response.run(request, **kwargs)
	
	if request.POST and request.POST.get('username', None):
		u = User.objects.get(username = request.POST.get('username', None))
		if u.get_profile().reset():
			success = True
		else:
			errors = 'Invalid username'
	else:
		errors = 'Invalid username'
	
	kwargs['data'] = { 'success' : success, 'errors' : errors }
	return response.run(request, **kwargs)
