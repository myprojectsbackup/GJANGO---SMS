from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from main.models import CustomUser, Staffs
from django.contrib import messages


def admin_home(request):
	return render(request, 'hod_templates/home_content.html')

def add_staff(request):
	return render(request, 'hod_templates/add_staff_template.html')

def add_staff_save(request):
	if request.method != 'POST':
		return HttpResponse('Not Allowed')
	else:
		first_name=request.POST.get('first_name')
		last_name=request.POST.get('last_name')
		username=request.POST.get('username')
		email=request.POST.get('email')
		password=request.POST.get('password')
		address=request.POST.get('address')

		try:
			user=CustomUser.objects.create_user(username=username, password=password, last_name=last_name, first_name=first_name, email=email, user_type=2)
			user.staffs.address=address
			user.save()
			messages.success(request, 'Staff Member Added Successful')
			return HttpResponseRedirect('/add_staff')
		except:
			messages.error(request, 'Failed to Add Staff Member, Retry Again!')
			return HttpResponseRedirect('/add_staff')
