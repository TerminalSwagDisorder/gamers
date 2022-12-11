from django import forms
import jsonfield

from .models import Game, Borrow

class GameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ["name", "genre", "delevoper", "year_published"]
		labels = {"name":"Game name", "genre":"Genre","delevoper":"Delevoper" , "year_published":"Publishing year"}
		widgets = {"name":forms.Textarea(attrs={"rows":1, "cols":30}), "genre":forms.Textarea(attrs={"rows":1, "cols":30}), "delevoper":forms.Textarea(attrs={"rows":1, "cols":30}), "year_published":forms.NumberInput(attrs={"min": 1, "max": 2999})}

class BorrowForm(forms.ModelForm):
	class Meta:
		model = Borrow
		fields = ["notes", "currentstatus"]
		labels = {"notes":"Notes", "currentstatus":"Check this box to be able to borrow this game"}
		widgets = {"notes":forms.Textarea(attrs={"cols":80})}
		#Form.has_changed()
