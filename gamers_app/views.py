from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import User as user

from .models import Game, Borrow, Gamer
from users.models import Profile
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
	games = Game.objects.order_by("id")
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
#Delete owned game
def delete_game(request, game_id):
  if request.method == "GET":
    game = get_object_or_404(Game, pk=game_id)
    if game.owner == request.user:
      game.delete()
      return redirect("gamers:index")
    else:
      messages.error(request, "You can only delete games that you have added.")
  return redirect("gamers:index")


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
			#Perform different validations
			# Check if the user has already borrowed 3 games
			borrow_count = Borrow.objects.filter(borrower=request.user, currentstatus=True).count()
			if borrow_count >= 3:
				messages.error(request, "You have already borrowed the maximum number of games (3), return one of your currently borrowed games to be able to borrow more games!")
				return redirect('gamers:gameborrow', game_id)
			if not form.cleaned_data["currentstatus"] == True:
				messages.error(request, "You cannot submit the form with an unchecked box!")
				return redirect('gamers:gameborrow', game_id)
			elif not form.has_changed():
				messages.error(request, "To borrow this game you must check the box!")
				return redirect('gamers:gameborrow', game_id)
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
			#Perform different validations
			if not form.cleaned_data["currentstatus"] == False:
				messages.error(request, "You cannot submit the form with a checked box!")
				return redirect('gamers:gameborrow', gameborrow.id)
			elif not form.has_changed():
				messages.error(request, "You cannot return an already returned game!")
				return redirect('gamers:gameborrow', gameborrow.id)
			else:
				form.save()
				return redirect("gamers:gameborrow", gameborrow.id)
	context = {"borrow":borrow, "gameborrow":gameborrow, "form":form}
	return render(request, "gamers/edit_borrow.html", context)
	
@login_required
def profile(request):
	userprofile = Profile.objects.filter(user = request.user)
	borrow = Borrow.objects.filter(borrower = request.user, currentstatus = True).order_by("-date_modified")
	games = Game.objects.filter(owner = request.user).order_by("id")
	context = {"userprofile":userprofile, "borrow":borrow, "games":games}
	return render(request, "gamers/profile.html", context)
		
