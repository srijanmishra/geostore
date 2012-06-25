from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from kestrel.graph.models import Node, Edge, Color

# kestrel people person
class Person(Node):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length = 32, default = '')
	address = models.CharField(max_length = 512, default = '')
	dateofbirth = models.DateField(null = True)
	gender = models.CharField(max_length = 1 , choices = (('M', 'Male'), ('F', 'Female'), ('N', 'Not Specified')), default = 'N')

# register handler for user
def create_person(sender, instance, created, **kwargs):
    if created:
		parent = Node.objects.get(id = settings.PEOPLE_ID)
		person = Person.objects.create(user = instance, name = instance.username, type = 'user', author = instance.username, parent = parent)
		person.add(user = settings.PEOPLE_ID, child = person)

post_save.connect(create_person, sender=User)

