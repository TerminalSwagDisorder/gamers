import jsonfield
import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
	#Book entity
	name = models.CharField(max_length = 100)
	authors = jsonfield.JSONField(blank = True, default = {"":"Author 1"})
	year_published = models.IntegerField(default = datetime.date.today().year)
	date_added = models.DateTimeField(auto_now_add = True)
	date_modified = models.DateTimeField(auto_now_add = True)
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	
	def __str__(self):
	#Returns a string representation of a book.
		return self.name

class Review(models.Model):
	#Review entity
	my_review = models.CharField(max_length = 400)
	stars = models.IntegerField(default = 5)
	unfinished = models.BooleanField(default = False)
	date_added = models.DateTimeField(auto_now_add = True)
	date_modified = models.DateTimeField(auto_now_add = True)
	book = models.ForeignKey(Book, on_delete = models.CASCADE)
	owner = models.ForeignKey(User, on_delete = models.CASCADE)

	#booksfield = models.ManyToManyField(Book)
	#Returns a string representation of a review.
	
	def __str__(self):
		return f"{self.my_review[:50]}..."

	class Meta:
		verbose_name_plural = "reviews"
