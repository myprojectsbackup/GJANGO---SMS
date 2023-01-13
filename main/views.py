from django.shortcuts import render
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from main.EmailBackEnd import EmailBackEnd

# Create your views here.

def home(request):
	return render(request, 'index.html')

def ShowLoginPage(request):
	return render(request, 'login_page.html')

def doLogin(request):
	if request.method!='POST':
		return HttpResponse("<h2>METHOD NOT ALLOWED</h2>")
	else:
		user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
		if user != None:
			login(request, user)
			return HttpResponseRedirect('/admin_home')

		else:
			messages.error(request, 'INVALID LOGIN DETAILS')
			return HttpResponseRedirect("/")

def GetUserDetails(request):
	if request.user!=None:
		return HttpResponse("User: "+request.user.email+" Usertype "+str(request.user.user_type))
	else:
		return HttpResponse("LOGIN FIRST")

def logout_user(request):
	logout(request)
	return HttpResponseRedirect ("/")