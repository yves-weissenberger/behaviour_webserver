from django.db import models
import datetime
from django.utils import timezone


#This defines a class known as Question which inherits
#from models.Model 
class Question(models.Model):

	#Ok, now lets give a couple of variables to this
	#this
	question_text = models.CharField(max_length=200)     #To do. Look up a bunch of different models
	pub_date = models.DateTimeField('date published')
	
	#Ok, now lets give this class a couple of methods
	def __unicode__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	was_published_recently.admin_order_field = 'pub_date'   #ok, lets give it a thing to order by
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
	question = models.ForeignKey(Question)   #not quite sure what this ForeignKey thing is...
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.choice_text
