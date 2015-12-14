from django.db import models

# Create your models here.
class job(models.Model):
	
	jobnumber = models.TextField()
	address = models.TextField()
	timestamp = models.DateTimeField()
	client = models.TextField(null=True)
	notes = models.TextField(null=True)

	councilassets = models.TextField(null=True)
	neighbours = models.TextField(null=True)
	letters = models.TextField(default='', null=True)
	img = models.TextField(default='', null=True)

	latitude = models.TextField(default='', null=True)
	longitude = models.TextField(default='', null=True)
	postcode = models.TextField(default='', null=True)

	def __str__(self):
		return self.jobnumber