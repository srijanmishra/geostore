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
	ctime = models.DateTimeField(auto_now_add = True)
	mtime = models.DateTimeField(auto_now = True)
	author = models.CharField(max_length = 256, default = '')
	parent = models.ForeignKey('self', related_name = 'pnode', default = ROOT_ID)
	network = models.ManyToManyField('self', through = 'Edge', related_name = 'endpoints', symmetrical = False)
	
	# KCW+ fields
	owner = models.ForeignKey('self', related_name = 'master', default = ROOT_ID)
	grroot = models.ForeignKey('self', null = True, related_name = 'gnode')
	level = models.IntegerField(default = 0)
	grlevel = models.IntegerField(default = 0)
	authorize = models.CharField(max_length = 512, default = 'info:edit:add:remove:list')
	
	def __unicode__(self):
		return '%s [%d]' % (self.name, self.id)
	
	# input user, action, iaction, color, icolor, acolor, delegate, udelegate
	def add(self, *args, **kwargs):
		if(self.parent.guard(user = kwargs.get('user', self.owner.id), action = kwargs.get('action', 'add'), iaction = kwargs.get('iaction', 'add'), color = kwargs.get('color', 'owner'), icolor = kwargs.get('icolor', 'all'))):
			if not self.id: 
				if not self.level:
					self.level = self.parent.level + 1 if self.parent.level >= 0 else self.parent.level - 1
				if not self.grlevel:
					self.grlevel = self.parent.grlevel
					self.grroot = self.parent.grroot
				if not self.authorize:
					self.authorize = self.parent.authorize
				super(Node, self).save()
				self.owner = self
				super(Node, self).save()
				edge = Edge(parent = self, child = kwargs.get('child', self.owner), type = 'user', color = 'owner', delegate = kwargs.get('udelegate', 'info:edit:add:remove:list'))
				edge.save()
			edge = Edge(parent = self.parent, child = self, type = self.type, color = kwargs.get('acolor', 'all'),  delegate = kwargs.get('delegate', 'info:edit:add:remove:list'))
			edge.save()
			self.parent.count = models.F('count') + 1;
			self.parent.save()
		else:
			raise Node.GuardException
	
	# input user, parent, action, iaction, color, icolor
	def remove(self, *args, **kwargs):
		if(self.guard(user = kwargs.get('user', -1), action = kwargs.get('action', 'remove'), iaction = kwargs.get('iaction', 'remove'), color = kwargs.get('color', 'owner'), icolor = kwargs.get('icolor', 'all'))):
			try: 
				Edge.objects.get(parent = kwargs.get('parent', self.parent), child = self).delete()
			except Exception, e: pass
			try:
				Edge.objects.filter(parent = self, type = 'user').delete()
			except Exception, e: pass
			parent = kwargs.get('parent', self.parent)
			parent.count = models.F('count') - 1;
			parent.save();
			self.delete()
		else:
			raise Node.GuardException
	
	# input user, action, iaction, color, icolor, type, lcolor
	def list(self, *args, **kwargs):
		if(self.guard(user = kwargs.get('user', -1), action = kwargs.get('action', 'list'), iaction = kwargs.get('iaction', 'list'), color = kwargs.get('color', 'owner'), icolor = kwargs.get('icolor', 'all'))):
			return Node.objects.filter(id__in = Edge.objects.filter(parent = self, type = kwargs.get('type', 'general'), color__contains = kwargs.get('lcolor', 'all')).values_list('child'))
		else:
			raise Node.GuardException
	
	# input user, action, iaction, color, icolor
	def edit(self, *args, **kwargs):
		if(self.guard(user = kwargs.get('user', -1), action = kwargs.get('action', 'edit'), iaction = kwargs.get('iaction', 'edit'), color = kwargs.get('color', 'owner'), icolor = kwargs.get('icolor', 'all'))):
			try:
				self.author = Node.objects.get(id = kwargs.get('user', -1)).name
			except: pass
			super(Node, self).save()
		else:
			raise Node.GuardException
	
	# input user, action, iaction, color, icolor
	def info(self, *args, **kwargs):
		if(self.guard(user = kwargs.get('user', -1), action = kwargs.get('action', 'info'), iaction = kwargs.get('iaction', 'info'), color = kwargs.get('color', 'owner'), icolor = kwargs.get('icolor', 'all'))):
			return self
		else:
			raise Node.GuardException
	
	# KCW+ guard authorize
	def guard(self, user = -1, action = 'edit', iaction = 'edit', color = 'owner', icolor = 'all', owner = True, custom = False):
		# check ownership, public auth and necessity
		if(owner and (user == self.owner.id or self.authorize.find('pb' + action) != -1 or (self.authorize.find(action) == -1 and user > 0))):
			return True
		
		# check anonymous user
		if(user < 0): return False
		
		# execute custom auth
		# if(custom): custom(id, user, action, iaction);
		
		# check group auth
		if(self.authorize.find('gr' + action) != -1):
			level = self.grlevel
			id = self.grroot
		else:
			level = self.level
			id = self.id
		
		# initialize
		moveup = level > -1
		level = level + 1 if moveup else -1*level + 1
		nodes = [self]

		# recursively check over delegation graph
		while(level):
			level -= 1;
			try:
				# find owner
				Edge.objects.get(parent__in = nodes, child = user, type = 'user', color__contains = color)
			except Exception, e:
				if level:
					# replace nodes with extended network
					if moveup:
						nodes = Edge.objects.filter(child__in = nodes, delegate__contains = iaction, color__contains = icolor).values_list('parent')
					else:
						nodes = Edge.objects.filter(parent__in = nodes, delegate__contains = iaction, color__contains = icolor).values_list('child')
			else:
				# auth success
				return True
		
		# auth fail
		return False

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
	type = models.CharField(max_length = 512, default = 'general')
	color = models.CharField(max_length = 512, default = 'all')
	
	# KCW+ fields
	delegate = models.CharField(max_length = 512, default = 'info:edit:add:remove:list')
	
	def __unicode__(self):
		return self.parent.__str__() + ' --> ' + self.child.__str__()

# kestrel graph color
class Color(Node):
	class Meta:
		proxy = True
	
	def add(self, *args, **kwargs):
		if not self.type: 
			self.type = 'color'
		self.name = ''.join([self.parent.name, '.', self.name])
		super(Color, self).add(*args, **kwargs)
