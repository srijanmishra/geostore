from django import forms
from django.core import validators
from django.contrib.auth.models import User
 
class RegistrationForm(forms.Form):
	username = forms.CharField(max_length = 30, required = True)
	email = forms.EmailField(max_length = 30, required = True)
	password1 = forms.CharField(widget=forms.PasswordInput, max_length = 30, required = True)
	password2 = forms.CharField(widget=forms.PasswordInput, max_length = 30, required = True)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username = username)
		except User.DoesNotExist:
			return username
		else:
			raise forms.ValidationError("Username is not available.")
	
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email = email)
		except User.DoesNotExist:
			return email
		else:
			raise forms.ValidationError("Email already registered.")
	
	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if password1 != password2:
			raise forms.ValidationError("Passwords do not match.")
			
		return password2
	
	def save(self, new_data):
		u = User.objects.create_user(new_data['username'], new_data['email'], new_data['password1'])
		u.is_active = False
		u.save()
		return u
