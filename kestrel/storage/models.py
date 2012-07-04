import os
from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage
from kestrel.graph.models import Node, Edge, Color

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

# kestrel storage directory
class Directory(Node):
	private = models.BooleanField(default = True)
	path = models.CharField(max_length = 512, default = '/')
	
	def add(self, *args, **kwargs):
		if not self.type: 
			self.type = 'directory'
		# remove / in name
		super(Directory, self).add(*args, **kwargs)
		try:
			os.mkdir(''.join([settings.STORAGE_PRIVATE_ROOT if self.private else settings.STORAGE_PUBLIC_ROOT, self.path, self.name]).replace('/', os.sep))
		except:
			raise Exception("Unable to create Directory" + ''.join([settings.STORAGE_PRIVATE_ROOT if self.private else settings.STORAGE_PUBLIC_ROOT, self.path, self.name]).replace('/', os.sep))
	
	def remove(self, *args, **kwargs):
		super(Directory, self).remove(*args, **kwargs)
		try:
			os.rmdir(''.join([settings.STORAGE_PRIVATE_ROOT if self.private else settings.STORAGE_PUBLIC_ROOT, self.path, self.name]).replace('/',os.sep))
		except:
			raise Exception("Unable to delete Directory")

# upload_to callable
def get_upload_path(instance, filename):
	d = Directory.objects.get(id = instance.parent.id)
	if not instance.name: instance.name = filename
	else : filename = instance.name
	return ''.join([settings.STORAGE_PRIVATE_ROOT if d.private else settings.STORAGE_PUBLIC_ROOT, d.path, d.name, '/', filename])

# kestrel storage file
class File(Node):
	file = models.FileField(upload_to = get_upload_path, max_length = 512, storage = OverwriteStorage())
	
	def add(self, *args, **kwargs):
		if not self.type: 
			self.type = 'file'
		# remove / in name
		super(File, self).add(*args, **kwargs)
