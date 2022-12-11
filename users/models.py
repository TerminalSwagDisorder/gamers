from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	
	def __str__(self):
		"""Returns a string representation of a user"""
		return self.description
