from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from main.models import CustomUser, Staffs, Courses, Students, Subjects
from django.contrib import messages
import datetime
from django.core.files.storage import FileSystemStorage
from main.forms import AddStudentForm

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
	form = AddStudentForm()
	return render(request, 'hod_templates/add_student_template.html', {'form': form})

def add_student_save(request):
	if request.method != 'POST':
		return HttpResponse('Method Not Allowed')

	else:
		form = AddStudentForm(request.POST, request.FILES)
		if form.is_valid():
			first_name=form.cleaned_data['first_name']
			last_name=form.cleaned_data['last_name']
			username=form.cleaned_data['username']
			email=form.cleaned_data['email']
			password=form.cleaned_data['password']
			address=request.POST.get('address')
			session_start =form.cleaned_data['session_start']
			session_end = form.cleaned_data['session_end']
			course_id = form.cleaned_data['course']
			sex = form.cleaned_data['sex']


			#uploading profile picture
			profile_pic=request.FILES['profile_pic']
			fs = FileSystemStorage()
			filename = fs.save(profile_pic.name,profile_pic)
			profile_pic_url = fs.url(filename)


			try:
				user=CustomUser.objects.create_user(username=username, password=password, last_name=last_name, first_name=first_name, email=email, user_type=3)
				user.students.address=address
				user.students.session_start_year = session_start
				user.students.session_end_year = session_end
				user.students.gender = sex
				course_obj = Courses.objects.get(id=course_id)
				user.students.course_id = course_obj
				user.students.prof_pic = profile_pic_url
				user.save()
				messages.success(request, 'Student Added Successful')
				return HttpResponseRedirect('/add_student')
			except:
				messages.error(request, 'Failed to Add Student, Retry Again!')
			return HttpResponseRedirect('/add_student')
		else:
			form=AddStudentForm(request.POST)
			return render(request, 'hod_templates/add_student_template.html', {'form': form})


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

def manage_staff(request):
	staffs=Staffs.objects.all()
	return render(request, 'hod_templates/manage_staff_template.html', {"staffs": staffs})

def manage_student(request):
	students=Students.objects.all()
	return render(request, 'hod_templates/manage_student_template.html', {"students": students})

def manage_course(request):
	courses = Courses.objects.all()
	return render(request, 'hod_templates/manage_course_template.html', {"courses": courses})

def manage_subject(request):
	subjects=Subjects.objects.all()
	return render(request, 'hod_templates/manage_subject_template.html', {"subjects": subjects})

def edit_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)
	return render(request, 'hod_templates/edit_staff_template.html', {"staff": staff, "id": staff_id})

def edit_staff_save(request):
	if request.method != 'POST':
		return HttpResponse('Method Not Allowed')

	else:
		staff_id= request.POST.get('staff_id')
		first_name= request.POST.get('first_name')
		last_name= request.POST.get('last_name')
		email= request.POST.get('email')
		username= request.POST.get('username')
		address= request.POST.get('address')

		try:
			user = CustomUser.objects.get(id=staff_id)
			user.first_name = first_name
			user.last_name = last_name
			user.username = username
			user.email = email
			user.save()

			staff_model = Staffs.objects.get(admin=staff_id)
			staff_model.address = address
			staff_model.save()
			messages.success(request, 'Staff Member Details Successfully Edited')
			return HttpResponseRedirect('/edit_staff/'+staff_id)
		except:
			messages.error(request, 'Failed to Edit Staff Member, Retry')
			return HttpResponseRedirect('/edit_staff/'+staff_id)

def edit_student(request, student_id):
	courses = Courses.objects.all()
	student = Students.objects.get(admin=student_id)
	return render(request, 'hod_templates/edit_student_template.html', {"student": student, "courses": courses, "id": student_id})

def edit_student_save(request):
	if request.method != 'POST':
		return HttpResponse('Method Not Allowed')

	else:
		student_id = request.POST.get('student_id')
		first_name=request.POST.get('first_name')
		last_name=request.POST.get('last_name')
		username=request.POST.get('username')
		email=request.POST.get('email')
		address=request.POST.get('address')
		session_start = request.POST.get('session_start')
		session_end = request.POST.get('session_end')
		course_id = request.POST.get('course')
		sex = request.POST.get('sex')

		#If condition when file is selected
		if request.FILES.get('profile_pic', False):
			profile_pic=request.FILES['profile_pic']  
			fs = FileSystemStorage() 
			filename = fs.save(profile_pic.name,profile_pic)   
			profile_pic_url = fs.url(filename)
		else:
			profile_pic_url = None

		
		try:
			user = CustomUser.objects.get(id = student_id)
			user.first_name = first_name
			user.last_name = last_name
			user.username = username
			user.email = email
			user.save()

			student=Students.objects.get(admin=student_id)
			student.address = address
			student.session_start_year = session_start
			student.session_end_year = session_end
			student.gender=sex

			course = Courses.objects.get(id=course_id)
			student.course_id=course
			if profile_pic_url != None:
				student.profile_pic=profile_pic_url
			student.save()
			messages.success(request, 'Student Details Successfully Edited')
			return HttpResponseRedirect('/edit_student/'+student_id)

		except:
			messages.error(request, 'Failed to Edit Student, Retry')
			return HttpResponseRedirect('/edit_student/'+student_id)

def edit_subject(request, subject_id):
	subject=Subjects.objects.get(id=subject_id)
	courses=Courses.objects.all()
	staffs=CustomUser.objects.filter(user_type=2)
	return render(request, 'hod_templates/edit_subject_template.html', {'subject': subject, 'courses': courses, 'staffs': staffs, "id":subject_id})

def edit_subject_save(request):
	if request.method != 'POST':
		return HttpResponse('<h2>METHOD NOT ALLOWED </h2>')
	else:
		subject_id=request.POST.get('subject_id')
		subject_name = request.POST.get('subject_name')
		staff_id = request.POST.get('staff')
		course_id = request.POST.get('course')
		
		try:
			subject=Subjects.objects.get(id=subject_id)
			subject.subject_name=subject_name
			staff = CustomUser.objects.get(id = staff_id)
			subject.staff_id=staff
			course = Courses.objects.get(id=course_id)
			subject.course_id=course
			subject.save()
			messages.success(request, 'Subject Successfully Edited')
			return HttpResponseRedirect('/edit_subject/'+subject_id)

		except:
			messages.error(request, 'Failed to Edit Subject, Retry')
			return HttpResponseRedirect('/edit_subject/'+subject_id)

def edit_course(request, course_id):
	course=Courses.objects.get(id=course_id)
	return render(request, 'hod_templates/edit_course_template.html', {'course': course, "id": course_id})

def edit_course_save(request):
	if request.method != 'POST':
		return HttpResponse('<h2>METHOD NOT ALLOWED </h2>')
	else:
		course_id=request.POST.get('course_id')
		course_name = request.POST.get('course')

		try:
			course = Courses.objects.get(id=course_id)
			course.course_name=course_name
			course.save()
			messages.success(request, 'Course Successfully Edited')
			return HttpResponseRedirect('/edit_course/'+course_id)

		except:
			messages.error(request, 'Failed to Edit Course, Retry')
			return HttpResponseRedirect('/edit_course/'+course_id)