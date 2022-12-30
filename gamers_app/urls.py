from django.urls import path
from . import views

app_name = "gamers"
urlpatterns = [
	#Home page
	path("", views.index, name = "index"),
	#Page that shows all games
	path("games", views.games, name = "games"),
	#Page for specific game borrow
	path("gameborrow/<int:games_id>/", views.gameborrow, name = "gameborrow"),
	#Page for all borrows
	path("borrows", views.borrows, name = "borrows"),
	#Page for adding a new game
	path("new_game/", views.new_game, name="new_game"),
	#Page for deleting own games
	path("games/<int:game_id>/delete/", views.delete_game, name = "delete"),
	#Page for adding a new borrow
	path("new_borrow/<int:game_id>/", views.new_borrow, name = "new_borrow"),
	#Page for returning a borrow
	path("edit_borrow/<int:game_id>/", views.edit_borrow, name = "edit_borrow"),
	#Profile page
	path("accounts/profile/", views.profile, name = "profile"),
]
