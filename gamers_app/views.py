from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Game, Borrow, Gamer
from .forms import GameForm, BorrowForm

#Custom exception
class StatusException(Exception):
	pass

# Create your views here.

#The home page for gamers
def index(request):
	return render(request, "gamers/index.html")
	
#Show all games	
def games(request):
	games = Game.objects.order_by("name")
	context = {"games":games}
	return render(request, "gamers/games.html", context)

#Borrows for a specific game
def gameborrow(request, games_id):
	games = Game.objects.get(id = games_id)
	borrow = games.borrow_set.order_by("-date_modified")
	borrowfilter = Borrow.objects.filter(game = games_id)
	context = {"games":games, "borrow":borrow, "borrowfilter":borrowfilter}
	return render(request, "gamers/gameborrow.html", context)

#All borrows
def borrows(request):
	borrows = Borrow.objects.order_by("game")
	context = {"borrows":borrows}
	return render(request, "gamers/borrows.html", context)

@login_required		
#Add new game
def new_game(request):
	if request.method != "POST":
		#No data submitted -> blank form
		form = GameForm()
	else:
		#POST data submitted
		form = GameForm(data = request.POST)
		if form.is_valid():
			new_game = form.save(commit = False)
			new_game.owner = request.user
			new_game.save()
			return redirect("gamers:games")
	context = {"form":form}
	return render(request, "gamers/new_game.html", context)

@login_required	
#Add new borrow	
def new_borrow(request, game_id):
	#if game is borrowed dont allow it to be borrowed
	games = Game.objects.get(id = game_id)
	if request.method != "POST":
		#No data submitted -> blank form
		form = BorrowForm()
	else:
		#POST data submitted
		form = BorrowForm(data = request.POST)
		if form.is_valid():
			#if not "currentstatus" in form.changed_data:
			#	raise StatusException("To borrow this game you must check the box!")
			if not form.cleaned_data["currentstatus"] == True:
				raise StatusException("You cannot submit the form with an unchecked box!")
			elif not form.has_changed():
				raise StatusException("To borrow this game you must check the box!")
			else:
				new_borrow = form.save(commit = False)
				new_borrow.game = games
				new_borrow.owner = request.user
				new_borrow.save()
				return redirect("gamers:gameborrow", game_id)
	context = {"games":games, "form":form}
	return render(request, "gamers/new_borrow.html", context)

@login_required	
#Edit an existing borrow
def edit_borrow(request, game_id):
	borrow = Borrow.objects.get(id = game_id)
	gameborrow = borrow.game
	#Authenticate user as object owner
	if borrow.borrower != request.user:
		raise Http404
	if request.method != "POST":
		#Initial request, prefill form with current data
		form = BorrowForm(instance = borrow)
	else:
		#POST data submitted
		form = BorrowForm(instance = borrow, data = request.POST)
		if form.is_valid():
			#if not "currentstatus" in form.changed_data:
			#	raise StatusException("To return this game you must uncheck the box!")
			if not form.cleaned_data["currentstatus"] == False:
				#print(form.fields["currentstatus"], form.cleaned_data["currentstatus"])
				raise StatusException("You cannot submit the form with a checked box!")
			elif not form.has_changed():
				raise StatusException("You cannot return an already returned game!")
			else:
				form.save()
				return redirect("gamers:gameborrow", gameborrow.id)
	context = {"borrow":borrow, "gameborrow":gameborrow, "form":form}
	return render(request, "gamers/edit_borrow.html", context)
	
'''
			#if not "currentstatus" in form.changed_data:
			#	raise StatusException("To borrow this game you must check the box!")
			if not "currentstatus" in form.changed_data == False:
				raise StatusException("You cannot submit the form with an unchecked box!")


				if not form.has_changed():
				raise StatusException("To return this game you must uncheck the box!")
				if not "currentstatus" in form.changed_data:
					raise StatusException("You cannot submit the form with a checked box!")
			elif form.has_changed() and "currentstatus" in form.changed_data:
				form.save()
				return redirect("gamers:gameborrow", gameborrow.id)
'''				
