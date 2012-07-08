import os, shutil
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
	root = models.SmallIntegerField(default = 0)
	path = models.CharField(max_length = 512, default = '/')
	
	def add(self, *args, **kwargs):
		if not self.type: 
			self.type = 'directory'
		d = Directory.objects.get(id = self.parent.id)
		self.path = d.path + d.name + '/'
		if not self.root:
			self.root = d.root
		if '/' in self.name:
			raise Exception("Invalid Directory Name" + self.name)
		super(Directory, self).add(*args, **kwargs)
		try:
			os.mkdir(''.join([settings.STORAGE_ROOT[self.root], self.path, self.name]).replace('/', os.sep))
		except:
			raise Exception("Unable to create Directory" + ''.join([settings.STORAGE_ROOT[self.root], self.path, self.name]).replace('/', os.sep))
	
	def remove(self, *args, **kwargs):
		super(Directory, self).remove(*args, **kwargs)
		try:
			shutil.rmtree(''.join([settings.STORAGE_ROOT[self.root], self.path, self.name]).replace('/',os.sep))
		except:
			raise Exception("Unable to Delete Directory")
	
	def rename(self, name, *args, **kwargs):
		try:
			os.rename(''.join([settings.STORAGE_ROOT[self.root], self.path, self.name]).replace('/',os.sep), ''.join([settings.STORAGE_ROOT[self.root], self.path, name]).replace('/',os.sep))
			self.name = name
			self.save()
		except:
			raise Exception("Unable to Rename Directory")
	
	def get_root(self, *args, **kwargs):
		return settings.STORAGE_NAMES[self.root]

# upload_to callable
def get_upload_path(instance, filename):
	d = instance.parent.directory
	if not instance.name: instance.name = filename
	else : filename = instance.name
	return ''.join([settings.STORAGE_ROOT[d.root], d.path, d.name, '/', filename])

# kestrel storage file
class File(Node):
	file = models.FileField(upload_to = get_upload_path, max_length = 512, storage = OverwriteStorage())
	mime = models.CharField(max_length = 512, default = 'application/force-download')
	
	def add(self, *args, **kwargs):
		if not self.type: 
			self.type = 'file'
		if '/' in self.name:
			raise Exception("Invalid File Name" + self.name)
		super(File, self).add(*args, **kwargs)
	
	def rename(self, name, *args, **kwargs):
		d = self.parent.directory
		try:
			os.rename(''.join([settings.STORAGE_ROOT[d.root], d.path, d.name, '/', self.name]).replace('/',os.sep), ''.join([settings.STORAGE_ROOT[d.root], d.path, d.name, '/', name]).replace('/',os.sep))
			self.name = name
			self.save()
		except:
			raise Exception("Unable to Rename File")
	
	def remove(self, *args, **kwargs):
		super(File, self).remove(*args, **kwargs)
		try:
			d = self.parent.directory
			os.remove(''.join([settings.STORAGE_ROOT[d.root], d.path, d.name, '/', self.name]).replace('/',os.sep))
		except WindowsError:
			pass
	
	def get_path(self, *args, **kwargs):
		d = self.parent.directory
		return ''.join([settings.STORAGE_ROOT[d.root], d.path, d.name, '/', self.name]).replace('/',os.sep)
	
	def get_public_url(self, *args, **kwargs):
		return settings.STORAGE_URLS[self.parent.directory.root]
