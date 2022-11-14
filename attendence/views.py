
from django.views.decorators import gzip
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from django.http import StreamingHttpResponse,HttpResponse, HttpResponseRedirect, JsonResponse
# import requests
from django.template.response import TemplateResponse

from .models import Students, StudentsLoginInfo, TeachersLoginInfo, User
from attendence_system.settings import BASE_DIR
from . import util
from .forms import SignUpForm, EditProfileForm 
from face_recognition.model import Predict

import datetime
import os
import cv2
from multiprocessing.pool import ThreadPool
import time
from .scanner import VideoCamera
import runpy

# Create your views here.

def home(request):
    context = {}
    if request.method == 'POST':
        teacher_obj = request.POST.get('id')
        # print(teacher_obj)
        # predict = 'Yahya Shaikh 15 MSCIT'
        # loginStudent(predict,request)
        context['scan'] = 'yes'
    return render(request, 'attendence/home.html', {'scan':context})

def login_user(request):
    if request.method == 'POST': #if someone fills out form , Post it 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:# if user exist
            login(request, user)
            messages.success(request,('Youre logged in'))
            user1 = User.objects.filter(id=request.user.id).first()
            teacher_login = TeachersLoginInfo.objects.create(
                teacher=user1,
                classes=request.POST['std'],
                subjects=request.POST['sub']
            )
            teacher_ob = teacher_login
            teacher_login.save()
            context = {
                'id':teacher_ob.id,
                'login':str(teacher_ob.time_of_login),
                'subject':teacher_ob.subjects,
                'class':teacher_ob.classes
            }
            teacher_ob = context
            request.session['login_info'] = context
            return redirect('home')
            # return render(request, 'attendence/home.html',{'login_info':context}) #routes to 'home' on successful login  
        else:
            messages.success(request,('Error logging in'))
            return redirect('login') #re routes to login page upon unsucessful login
    else:
        return render(request, 'attendence/login.html', {})

def logout_user(request):
    print("YES")
    logout(request)
    messages.success(request,('Youre now logged out'))
    if 'login_info' in request.session:
        del request.session['login_info']
    # if 'student_login' in request.session:
    #     del request.session['student_login']
    return redirect('login')

def register_user(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ('Youre now registered'))
            return redirect('home')
    else: 
        form = SignUpForm() 

    context = {'form': form}
    return render(request, 'attendence/register.html', context)

def edit_profile(request):
    if request.method =='POST':
        form = EditProfileForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You have edited your profile'))
            return redirect('home')
    else: 		#passes in user information 
        form = EditProfileForm(instance= request.user) 

    context = {'form': form}
    return render(request, 'attendence/edit_profile.html', context)
    #return render(request, 'authenticate/edit_profile.html',{})



def change_password(request):
    if request.method =='POST':
        form = PasswordChangeForm(data=request.POST, user= request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('You have edited your password'))
            return redirect('home')
    else: 		#passes in user information 
        form = PasswordChangeForm(user= request.user) 

    context = {'form': form}
    return render(request, 'attendence/change_password.html', context)

face_cascade = cv2.CascadeClassifier('C:/Users/Admin/Downloads/Deeplearning/src/data/haarcascade_frontalface_alt2.xml')

t = 0

def gen(camera,request):
    global t
    if camera != None:
        pool = ThreadPool(processes=2)
        tool = pool.apply_async(timer)
        while t < 5:
            if t >= 5:
                break
            g = pool.apply_async(camera.get_frame)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + g.get() + b'\r\n\r\n')
    t = 0
    predict = Predict.predict()
    # predict = 'Yahya Shaikh 15 MSCIT'
    loginStudent(predict,request)

session = None
def loginStudent(predict,request):
    global session
    lst = predict.split()
    std = Students.objects.get(
        first_name=lst[0],
        last_name=lst[1],
        roll=lst[2],
        std=lst[3]
        )
    ids = request.session['login_info']['id']
    obj = TeachersLoginInfo.objects.get(id=ids)
    if std:
        StudentLogin = StudentsLoginInfo.objects.create(
            student=std,
            teacher=obj,
            time_of_login=request.session['login_info']['login']
        )
        StudentLogin.save()
        context = {
            'first_name':std.first_name,
            'last_name':std.last_name,
            'roll':std.roll,
            'std':std.std,
            'sub':obj.subjects,
            'class':obj.classes,
            'time':str(obj.time_of_login)
        }
        session = context
        request.session['student_login'] = context
        # request.session.modified = True
        # print(request.session.keys())
        # print(request.session['student_login'])
        # return render(request,'attendence/details.html',{'context':context})

def respond(request):   
    return render(request,'attendence/details.html',{'context':session})

def timer():
    global t
    while t < 5:
        print("WORKING>>>")
        time.sleep(5)
        t+=5

@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam,request), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

def addStudents(request):
    print(BASE_DIR)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll = request.POST.get('roll')
        std = request.POST.get('std')
        student = Students.objects.create(
            first_name=first_name,
            last_name=last_name,
            roll=roll,
            std=std
        )
        student.save()
        direct = '' + first_name+' '+last_name+' '+str(roll)+' '+std+''
        parent_dir = os.path.join(BASE_DIR,'face_recognition/students/'+direct)
        try: 
            os.mkdir(parent_dir) 
        except OSError as error: 
            print(error)
        util.video_to_frames(parent_dir)
        # student.save()
        redirect('home')
    return render(request,'attendence/students.html')