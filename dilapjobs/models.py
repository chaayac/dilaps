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

	latitude = models.TextField(default='', null=True)
	longitude = models.TextField(default='', null=True)
	postcode = models.TextField(default='', null=True)

	status = models.TextField(default='Incomplete')

	def __str__(self):
		return self.jobnumber
		
	def getNeighbours(self):
		return self.neighbours.split('|')
	def getLetters(self):
		return self.letters.split('|')
	def getCouncilAssets(self):
		return self.councilassets.split('|')
	def getNotes(self):
		if (len(self.notes.split('|')) == 2):
			return self.notes.split('|')[1]
		else:
			return ''
	def getUser(self):
		return self.notes.split('|')[0]


class logs(models.Model):
	timestamp = models.DateTimeField()
	logtext = models.TextField(default='', null=True)

	def __str__(self):
		return self.logtext