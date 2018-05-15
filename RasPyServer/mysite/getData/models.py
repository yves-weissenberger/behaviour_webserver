from django.db import models


class box(models.Model):

	box_nr = models.CharField(max_length=4)
	box_type = models.CharField(max_length=200)
	

	def __unicode__(self):
		return self.box_nr
	


	"""
	def getMouseID
	def getTask
	def setTask
	def WaterIntake
	"""




