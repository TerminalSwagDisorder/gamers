from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Book, Review
from .forms import BookForm, ReviewForm

# Create your views here.
def index(request):
	'''The home page for crazy book club'''
	return render(request, "gamers/index.html")
		
def books(request):
	'''Show all books'''
	books = Book.objects.order_by("date_added")
	context = {"books":books}
	return render(request, "gamers/books.html", context)

#Reviews for a specific book
def bookreview(request, books_id):
	reviews = Book.objects.get(id = books_id)
	review = reviews.review_set.order_by("date_added")
	context = {"reviews":reviews, "review":review}
	return render(request, "gamers/bookreview.html", context)

#Reviews for all books
def allreviews(request):
	review = Review.objects.order_by("book")
	context = {"review":review}
	return render(request, "gamers/reviews.html", context)

@login_required		
#Add new book
def new_book(request):
	'''Add a new book'''
	if request.method != "POST":
		#No data submitted -> blank form
		form = BookForm()
	else:
		#POST data submitted
		form = BookForm(data = request.POST)
		if form.is_valid():
			new_book = form.save(commit = False)
			new_book.owner = request.user
			new_book.save()
			return redirect("gamers:books")
	context = {"form":form}
	return render(request, "gamers/new_book.html", context)

@login_required	
#Add new review	
def new_review(request, book_id):
	'''Add a new review'''
	books = Book.objects.get(id = book_id)
	if request.method != "POST":
		#No data submitted -> blank form
		form = ReviewForm()
	else:
		#POST data submitted
		form = ReviewForm(data = request.POST)
		if form.is_valid():
			new_review = form.save(commit = False)
			new_review.book = books
			new_review.owner = request.user
			new_review.save()
			return redirect("gamers:bookreview", book_id)
	context = {"books":books, "form":form}
	return render(request, "gamers/new_review.html", context)

@login_required	
#Edit an existing review
def edit_review(request, book_id):
	'''Edit an existing experience'''
	review = Review.objects.get(id = book_id)
	bookreview = review.book
	#Authenticate user as object owner
	if bookreview.owner != request.user:
		raise Http404
	if request.method != "POST":
		#Initial request, prefill form with current data
		form = ReviewForm(instance = review)
	else:
		#POST data submitted
		form = ReviewForm(instance = review, data = request.POST)
		if form.is_valid():
			form.save()
			return redirect("gamers:bookreview", bookreview.id)
	context = {"review":review, "bookreview":bookreview, "form":form}
	return render(request, "gamers/edit_review.html", context)
