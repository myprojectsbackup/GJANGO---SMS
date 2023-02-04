from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from main.models import CustomUser, Staffs, Courses, Students, Subjects
from django.contrib import messages
import datetime


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

def add_course(request):
	return render(request, 'hod_templates/add_course_template.html')

def add_course_save(request):
	if request.method != 'POST':
		return HttpResponse('Not Allowed')

	else:
		course=request.POST.get('course')

		try:
			course_model = Courses(course_name=course)
			course_model.save()
			messages.success(request, 'Course Successfully Added')
			return HttpResponseRedirect('/add_course')
		except:
			messages.error(request, 'Failed to Add Course, Retry')
			return HttpResponseRedirect('/add_course')

def add_student(request):
	courses=Courses.objects.all()    #for courses to show on the add students page
	return render(request, 'hod_templates/add_student_template.html', {"courses":courses})

def add_student_save(request):
	if request.method != 'POST':
		return HttpResponse('Method Not Allowed')

	else:
		first_name=request.POST.get('first_name')
		last_name=request.POST.get('last_name')
		username=request.POST.get('username')
		email=request.POST.get('email')
		password=request.POST.get('password')
		address=request.POST.get('address')
		session_start = request.POST.get('session_start')
		session_end = request.POST.get('session_end')
		course_id = request.POST.get('course')
		sex = request.POST.get('sex')


		try:
			user=CustomUser.objects.create_user(username=username, password=password, last_name=last_name, first_name=first_name, email=email, user_type=3)
			user.students.address=address
			course_obj = Courses.objects.get(id=course_id)
			user.students.course_id = course_obj
			user.students.session_start_year = session_start
			user.students.session_end_year = session_end
			user.students.gender = sex
			user.students.prof_pic = ""
			user.save()
			messages.success(request, 'Student Added Successful')
			return HttpResponseRedirect('/add_student')
		except:
			messages.error(request, 'Failed to Add Student, Retry Again!')
		return HttpResponseRedirect('/add_student')

def add_subject(request):
	courses=Courses.objects.all()    #for courses to show on the add subject page
	staffs=CustomUser.objects.filter(user_type=2) #for staff members to show in the add subject page
	return render(request, 'hod_templates/add_subject_template.html', {"staffs": staffs, "courses":courses})

def add_subject_save(request):
	if request.method != 'POST':
		return HttpResponse('Method Not Allowed')

	else:
		subject_name=request.POST.get("subject_name")
		course_id=request.POST.get("course")
		course=Courses.objects.get(id=course_id)
		staff_id=request.POST.get("staff")
		staff=CustomUser.objects.get(id=staff_id)

		try:
			subject=Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
			subject.save()
			messages.success(request, 'Subject Successfully Added')
			return HttpResponseRedirect('/add_subject')
		except:
			messages.error(request, 'Failed to Add Subject, Retry')
			return HttpResponseRedirect('/add_subject')