from django.urls import path
from . import views

app_name = "gamers"
urlpatterns = [
	#Home page
	path("", views.index, name = "index"),
	#Page that shows all books
	path("books", views.books, name = "books"),
	#Page for specific book reviews
	path("reviews/<int:books_id>/", views.bookreview, name = "bookreview"),
	#Page for all reviews
	path("allreviews", views.allreviews, name = "allreviews"),
	#Page for adding a new book
	path("new_book/", views.new_book, name="new_book"),
	#Page for adding a new review
	path("new_review/<int:book_id>/", views.new_review, name = "new_review"),
	#Page for editing an existing review
	path("edit_review/<int:book_id>/", views.edit_review, name = "edit_review"),
]
