from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as user
from .models import Profile

#Create your views here
def register(request):
	'''Register a new user'''
	if request.method != "POST":
		#No data submitted -> blank form
		form = UserCreationForm()
	else:
		#POST data submitted
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			new_user = form.save()
			#Log the user in and redirect to home page
			login(request, new_user)
			return redirect("gamers:index")
	#Display an empty or invalid form
	context = {"form":form}
	return render(request, "registration/register.html", context)

@login_required
def profile(request):
	userprofile = Profile.objects.filter(user = request.user)
	context = {"userprofile":userprofile}
	return render(request, "registration/profile.html")
