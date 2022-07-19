#import datetime
#import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from school_portal.IdBackEnd import IdBackEnd
from school_portal.models import CustomUser, ClassLevel, SessionYearModel
from portal_system import settings

# Create your views here.
def showLogin(request):
    return render(request, 'school/login_page.html')

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        
        user=IdBackEnd.authenticate(request,username=request.POST.get("school_id"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.id+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")