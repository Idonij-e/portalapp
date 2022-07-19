#import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from school_portal.forms import AddStudentForm, EditStudentForm
from school_portal.models import CustomUser, Administrator, Staff, ClassLevel, Subject, Student, SessionYearModel


def admin_home(request):
    student_count1=Student.objects.all().count()
    staff_count=Staff.objects.all().count()
    subject_count=Subject.objects.all().count()
    course_count=ClassLevel.objects.all().count()

    course_all=ClassLevel.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subject.objects.filter(course_id=course.id).count()
        students=Student.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subject.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=ClassLevel.objects.get(id=subject.course_id.id)
        student_count=Student.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    administrators=Administrator.objects.all()

    staffs=Staff.objects.all()
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subject.objects.filter(staff_id=staff.admin.id)
        staff_name_list.append(staff.admin.username)

    students_all=Student.objects.all()
    student_name_list=[]
    for student in students_all:
        student_name_list.append(student.admin.username)

    return render(request,"admin_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"student_name_list":student_name_list,"administrators":administrators,})

def add_staff(request):
    return render(request,"admin_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,password=password,user_type=2)
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request,"admin_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=ClassLevel(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form=AddStudentForm()
    return render(request,"admin_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            password=form.cleaned_data["password"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(password=password,first_name=first_name,last_name=last_name,user_type=3)
                course_obj=ClassLevel.objects.get(id=course_id)
                user.students.course_id=course_obj
                session_year=SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id=session_year
                user.students.gender=sex
                user.students.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "admin_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses=ClassLevel.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"admin_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=ClassLevel.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subject(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs=Staff.objects.all()
    return render(request,"admin_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students=Student.objects.all()
    return render(request,"admin_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses=ClassLevel.objects.all()
    return render(request,"admin_template/manage_class_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subject.objects.all()
    return render(request,"admin_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staff.objects.get(admin=staff_id)
    return render(request,"admin_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        #first_name=request.POST.get("first_name")
        #last_name=request.POST.get("last_name")
        #email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            #user.email=email
            user.username=username
            user.save()

            staff_model=Staff.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Student.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    form.fields['profile_pic'].initial=student.profile_pic
    return render(request,"admin_template/edit_student_template.html",{"form":form,"id":student_id,"first_name":student.admin.first_name})

def edit_student_save(request):
    #check if code deletes student_id on save
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.save()

                student=Student.objects.get(admin=student_id)
                student.address=address
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender=sex
                course=ClassLevel.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Student.objects.get(admin=student_id)
            return render(request,"admin_template/edit_student_template.html",{"form":form,"id":student_id,"first_name":student.user.first_name})

def edit_subject(request,subject_id):
    subject=Subject.objects.get(id=subject_id)
    courses=ClassLevel.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"admin_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            subject=Subject.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=ClassLevel.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=ClassLevel.objects.get(id=course_id)
    return render(request,"admin_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=ClassLevel.objects.get(id=course_id)
            print(ClassLevel.course_name)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


def manage_session(request):
    return render(request,"admin_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"admin_template/admin_profile.html",{"user":user})
    

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        
        if request.FILES.get('admin_profile_pic',False):
            admin_profile_pic=request.FILES['admin_profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(admin_profile_pic.name,admin_profile_pic)
            admin_profile_pic_url=fs.url(filename)
        else:
            admin_profile_pic_url=None

        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                 customuser.set_password(password)
            customuser.save()

            administrator=Administrator.objects.get(admin=customuser.id)
            if admin_profile_pic_url!=None:
                administrator.admin_profile_pic=admin_profile_pic_url
            administrator.save()

            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def admin_send_notification_student(request):
    students=Student.objects.all()
    return render(request,"admin_template/student_notification.html",{"students":students})

def admin_send_notification_staff(request):
    staffs=Staff.objects.all()
    return render(request,"admin_template/staff_notification.html",{"staffs":staffs})

#@csrf_exempt
#def send_student_notification(request):
#    id=request.POST.get("id")
#    id=request.POST.get("id")
#    id=request.POST.get("id")
#    message=request.POST.get("message")
#    student=Students.objects.get(admin=id)
#    token=student.fcm_token
#    url="https://fcm.googleapis.com/fcm/send"
#    body={
#        "notification":{
#            "title":"Student Management System",
#            "body":message,
#            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
#            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
#        },
#        "to":token
#    }
#    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
#    data=requests.post(url,data=json.dumps(body),headers=headers)
#    notification=NotificationStudent(student_id=student,message=message)
#    notification.save()
#    print(data.text)
#    return HttpResponse("True")

#@csrf_exempt
#def send_staff_notification(request):
#    id=request.POST.get("id")
#    message=request.POST.get("message")
#    staff=Staffs.objects.get(admin=id)
#    token=staff.fcm_token
#    url="https://fcm.googleapis.com/fcm/send"
#    body={
#        "notification":{
#            "title":"Student Management System",
#            "body":message,
#            "click_action":"https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
#            "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
#        },
#        "to":token
#    }
#    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
#    data=requests.post(url,data=json.dumps(body),headers=headers)
#    notification=NotificationStaffs(staff_id=staff,message=message)
#    notification.save()
#    print(data.text)
#    return HttpResponse("True")

