import datetime, random, sha, pytz
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from kestrel.graph.models import Node, Edge, Color
from kestrel.storage.models import File

# kestrel people person
class Person(Node):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length = 32, default = '')
	address = models.CharField(max_length = 512, default = '')
	dateofbirth = models.DateField(null = True)
	gender = models.CharField(max_length = 1 , choices = (('M', 'Male'), ('F', 'Female'), ('N', 'Not Specified')), default = 'N')
	photo = models.OneToOneField(File)
	activation_key = models.CharField(max_length = 40, null = True)
	key_expires = models.DateTimeField(null = True)
	credits = models.IntegerField(default = 50)
	
	def verify(self):
		salt = sha.new(str(random.random())).hexdigest()[:5]
		self.activation_key = sha.new(salt + self.user.username).hexdigest()
		self.key_expires = datetime.datetime.today().replace(tzinfo = pytz.UTC) + datetime.timedelta(settings.PEOPLE_VERIFY_EXPIRY)
		self.save()
		self.user.is_active = False
		self.user.save()
		email = EmailMessage(settings.PEOPLE_VERIFY_SUBJECT, 
					settings.PEOPLE_VERIFY_BODY % { 'username' : self.user.username, 'verify' : self.activation_key }, to=[ self.user.email ])
		return email.send()
	
	def confirm(self, code):
		if self.activation_key == code and self.key_expires > datetime.datetime.today().replace(tzinfo = pytz.UTC):
			self.user.is_active = True
			self.user.save()
			return True
		return False
	
	def reset(self):
		salt = sha.new(str(random.random())).hexdigest()[:5]
		password = sha.new(salt + self.user.username).hexdigest()[:8]
		self.user.set_password(password)
		self.user.save()
		email = EmailMessage(settings.PEOPLE_RESET_SUBJECT, 
					settings.PEOPLE_RESET_BODY % { 'username' : self.user.username, 'password' : password }, to=[ self.user.email ])
		return email.send()

# register handler for user
def create_person(sender, instance, created, **kwargs):
    if created:
		parent = Node.objects.get(id = settings.PEOPLE_ID)
		file = File(name = instance.username + '.png', author = instance.username, parent = parent, mime = 'image/png')
		file.add(user = settings.PEOPLE_ID)
		person = Person(user = instance, name = instance.username, type = 'user', author = instance.username, parent = parent, photo = file)
		person.add(user = settings.PEOPLE_ID)
		person.add(user = settings.PEOPLE_ID, parent = person, ecolor = 'owner.link')
		
		file.owner = person
		file.save()
		person.owner = person
		person.save()

post_save.connect(create_person, sender=User)

