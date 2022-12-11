from django import forms
import jsonfield

from .models import Book, Review

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ["name", "authors", "year_published"]
		labels = {"name":"Book name", "authors":"Authors", "year_published":"Publishing year"}
		widgets = {"name":forms.Textarea(attrs={"rows":1, "cols":30}), "year_published":forms.NumberInput(attrs={"min": 1, "max": 2999})}

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ["my_review", "stars", "unfinished"]
		labels = {"my_review":"Review", "stars":"Stars", "unfinished":"Unfinished?"}
		widgets = {"my_review":forms.Textarea(attrs={"cols":80}), "stars":forms.NumberInput(attrs={"min": 0, "max": 10})}

