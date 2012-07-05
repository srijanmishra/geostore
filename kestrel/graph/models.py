from django.db import models
import exceptions

ROOT_ID = 0

# kestrel graph node
class Node(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 256, default = '')
	type = models.CharField(max_length = 256, default = 'general')
	desc = models.CharField(max_length = 512, default = '')
	count = models.IntegerField(default = 0)
	links = models.IntegerField(default = 0)
	ctime = models.DateTimeField(auto_now_add = True)
	mtime = models.DateTimeField(auto_now = True)
	author = models.CharField(max_length = 256, default = '')
	owner = models.ForeignKey('self', related_name = 'master', default = ROOT_ID)
	parent = models.ForeignKey('self', related_name = 'pnode', default = ROOT_ID)
	network = models.ManyToManyField('self', through = 'Edge', related_name = 'endpoints', symmetrical = False)
	
	def __unicode__(self):
		return '%s [%s] [%d]' % (self.name, self.type, self.id)
	
	def add(self, user = None, parent = None, ecolor = 'all', action = 'add', owner = True, custom = False, override = [],
		inherit = ['info', 'edit', 'add', 'remove', 'list', 'link', 'unlink'], auth = 'N', color = 'all', ucolor = 'owner', grroot = None, level = 0, grlevel = 0, **kwargs):
		if not parent : parent = self.parent
		if not user: user = self.owner.id
		
		if(parent.guard(user = user, action = action, owner = owner, custom = custom)):
			if not self.id: 
				self.save()
				
				# inherit guards
				gs = Guard.objects.filter(node = parent, action__in = inherit)
				for g in gs:
					gn = Guard(node = self, auth = g.auth, action = g.action, color = g.color, ucolor = g.ucolor, grroot = g.grroot, 
						level = g.level + 1 if g.level >= 0 else g.level -1, grlevel = g.grlevel)
					gn.save()
				
				# override guards
				for action in override:
					gn = Guard(node = self, auth = auth, action = action, color = color, ucolor = ucolor, grroot = grroot, level = level, grlevel = grlevel)
					gn.save()
				
				# create owner link
				uedge = Edge(parent = self, child = self.owner, type = 'user', color = 'owner.link')
				uedge.save()
			
			# add child
			edge = Edge(parent = parent, child = self, type = self.type, color = ecolor)
			edge.save()
			parent.count = models.F('count') + 1;
			parent.save()
		else:
			raise Node.GuardException
	
	def link(self, user = -1, action = 'link', owner = True, custom = False, parent = None, color = 'all.link',  **kwargs):
		if(self.guard(user = user, action = action, owner = owner, custom = custom)):
			if not parent: parent = self.parent
			edge = Edge(parent = parent, child = self, type = self.type, color = color)
			edge.save()
			sef.parent.links = models.F('links') + 1
			self.parent.save()
		else:
			raise Node.GuardException
			
	def remove(self, user = -1, action = 'remove', owner = True, custom = False,  **kwargs):
		if(self.guard(user = user, action = action, owner = owner, custom = custom)):
			try: 
				Edge.objects.filter(parent = self.parent, child = self).delete()
			except Exception: pass
			try:
				Edge.objects.filter(parent = self, type = 'user').delete()
			except Exception: pass
			sef.parent.count = models.F('count') - 1;
			self.parent.save();
			self.delete()
		else:
			raise Node.GuardException
		
	def unlink(self, user = -1, action = 'unlink', owner = True, custom = False, parent = None,  **kwargs):
		if(self.guard(user = user, action = action, owner = owner, custom = custom)):
			if not parent: parent = self.parent
			try: 
				Edge.objects.filter(parent = parent, child = self).delete()
			except Exception: pass
			sef.parent.links = models.F('links') - 1
			self.parent.save()
		else:
			raise Node.GuardException
	
	def list(self, user = -1, action = 'list', owner = True, custom = False, type = 'general', lcolor = 'all', *args, **kwargs):
		if(self.guard(user = user, action = action, owner = owner, custom = custom)):
			return Node.objects.filter(id__in = Edge.objects.filter(parent = self, type = type, color__contains = lcolor).values_list('child'))
		else:
			raise Node.GuardException
	
	def edit(self, user = -1, action = 'edit', owner = True, custom = False, **kwargs):
		if(self.guard(user = user, action = action, owner = owner, custom = custom)):
			try:
				self.author = Node.objects.get(id = kwargs.get('user', -1)).name
			except: pass
			super(Node, self).save()
		else:
			raise Node.GuardException
	
	def info(self, user = -1, action = 'info', owner = True, custom = False, **kwargs):
		if(self.guard(user = user, action = action, owner = owner, custom = custom)):
			return self
		else:
			raise Node.GuardException
	
	# KCW+ guard authorize
	def guard(self, user = -1, action = 'edit', owner = True, custom = False):
		# check ownership
		if(owner and user == self.owner.id):
			return True
		
		try:
			g = Guard.objects.get(node = self, action = action)
			if g.auth == 'P': return True
			
			# execute custom auth
			# if(custom): 
				# result = custom(id, user, action)
				# if result: return True
			
			if g.auth == 'G':
				level = g.grlevel
				id = g.grroot
			else:
				level = g.level
				id = self
			
			moveup = level > -1
			level = level + 1 if moveup else -1*level + 1
			nodes = [id]
			
			# recursively check over delegation graph
			while level:
				level -= 1;
				try:
					# find owner
					Edge.objects.get(parent__in = nodes, child = user, type = 'user', color__contains = g.ucolor)
					# auth success
					return True
				except Edge.DoesNotExist:
					if level:
						# replace nodes with extended network
						if moveup:
							nodes = Edge.objects.filter(child__in = nodes, color__contains = g.color).values_list('parent')
						else:
							nodes = Edge.objects.filter(parent__in = nodes, color__contains = g.color).values_list('child')
			
			# auth fail
			return False
			
		except Guard.DoesNotExist:
			if(user > -1): return True
			else: return False
		
	# guard exception
	class GuardException(exceptions.Exception):
		def __init__(self):
			return
		
		def __str__(self):
			print  "", "Unable to Authorize"


# kestrel graph edge
class Edge(models.Model):
	id = models.AutoField(primary_key = True)
	parent = models.ForeignKey(Node, related_name = 'pedge')
	child = models.ForeignKey(Node, related_name = 'cedge')
	type = models.CharField(max_length = 256, default = 'general')
	color = models.CharField(max_length = 1024, default = 'all')
	
	def __unicode__(self):
		return self.parent.__str__() + ' --' + self.color + '--> ' + self.child.__str__()

# kestrel graph color
class Color(Node):
	class Meta:
		proxy = True
	
	def add(self, *args, **kwargs):
		if not self.type: 
			self.type = 'color'
		self.name = ''.join([self.parent.name, '.', self.name])
		super(Color, self).add(*args, **kwargs)

# kestrel graph guard
class Guard(models.Model):
	node = models.ForeignKey(Node, related_name = 'gnode')
	auth = models.CharField(max_length = 2, default = 'N') # P=public G=group N=normal
	action = models.CharField(max_length = 256, default = 'edit')
	color = models.CharField(max_length = 512, default = 'all')
	ucolor = models.CharField(max_length = 512, default = 'owner')
	grroot = models.ForeignKey(Node, null = True, related_name = 'grnode')
	level = models.IntegerField(default = 0)
	grlevel = models.IntegerField(default = 0)
