import jsonfield
import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Game(models.Model):
	#Game entity
	owner = models.ForeignKey(User, on_delete = models.CASCADE, default = 3)
	name = models.CharField(max_length = 100)
	genre = models.CharField(max_length = 100)
	developer = models.CharField(max_length = 100)
	year_published = models.IntegerField(default = datetime.date.today().year)
	date_added = models.DateTimeField(auto_now_add = True)
	date_modified = models.DateTimeField(auto_now = True)

	
	def __str__(self):
	#Returns a string representation of a game
		return self.name

class Borrow(models.Model):
	#Borrow entity
	game = models.ForeignKey(Game, on_delete = models.CASCADE)
	borrower = models.ForeignKey(User, on_delete = models.CASCADE, default = 3)
	currentstatus = models.BooleanField(default = False)
	notes = models.CharField(max_length = 400, blank = True)
	date_added = models.DateTimeField(auto_now_add = True)
	date_modified = models.DateTimeField(auto_now = True)

	
	#def __str__(self):
	#Returns a string representation of a borrow
		#return self.currentstatus
		#f"{self.currentstatus[:50]}..."

class Gamer(models.Model):
	#Gamer entity
	gameowner = models.ForeignKey(Game, on_delete = models.CASCADE)
	gameborrower = models.ForeignKey(Borrow, on_delete = models.CASCADE)
	gameuser = models.ForeignKey(User, on_delete = models.CASCADE, default = 3)
	borrowedfrom = models.BooleanField(default = False)
	
	#def __str__(self):
	#Returns a string representation of a gamer
		#return self.gameuser
