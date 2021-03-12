from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from .models import *
from .serializers import *
from django.views import View
# Create your views here.
'''
class Login(View):
    def get(self,request):
        return render(request,"sua\\login.html")
    def post(self,request):
        req=request.POST  #req is a dict    
        User_NetID=request.POST['NetID']
        User_Password=request.POST['Password']
        if (req["Remember_me"]):
            print("Yes")#TODO
        user = authenticate(username=User_NetID, password=User_Password)
        if (user is not None):   
            login(request,user)
            return redirect(index)         
        else:
            return HttpResponse("登录失败!")
@login_required
def index(request):
    NetID=request.user.username
    context={}
    context['suahours']=request.user.studentinfo.get_suahours()
    context['User_NetID']=NetID
    sua_all=request.user.studentinfo.suas.all()
    paginator=Paginator(sua_all,10)
    page=request.GET.get('page')#获取请求参数
    try:
        activity=paginator.page(page)
    except PageNotAnInteger:
        activity=paginator.page(1)
    except InvalidPage:
        return HttpResponse("Bad Request")
    except EmptyPage:
        activity=paginator.page(paginator.num_pages)
    context['Activity']=activity#TODO：activity初值
    return render(request,"sua\\index.html",context)
@login_required
def Logout(request):
    logout(request)
    return HttpResponse("退出登录成功!")
@login_required
def changepassword(request):
    if request.method=='GET':
        return render(request,"sua\\changepassword.html")
    else:
        Old=request.POST['Old_Password']
        user = authenticate(username=request.user.username, password=Old)
        if (user is not None):
            user.set_password(request.POST['New_Password'])
            user.save()
            return HttpResponse("修改密码成功！")
        else:
            return HttpResponse("原密码错误！")
@login_required
def applications(request):
    if request.method=='GET':
        return render(request,"sua\\applications.html")
    else:
        return HttpResponse("TODO")
'''
#以上是Django的视图函数
#以下是DRF的视图函数 
def Login(request):
    req=request.POST  #req is a dict    
    User_NetID=request.POST['NetID']
    User_Password=request.POST['Password']
    if (req["Remember_me"]):
        print("Yes")#TODO
    user = authenticate(username=User_NetID, password=User_Password)
    if (user is not None):   
        login(request,user)
        return HttpResponse("Yes")       
    else:
        return HttpResponse("No")
@login_required
def index(request):
    NetID=request.user.username
    print(NetID)
    context={}
    context['suahours']=request.user.studentinfo.get_suahours()
    context['User_NetID']=NetID
    sua_all=request.user.studentinfo.suas.all()
    paginator=Paginator(sua_all,10)
    page=request.GET.get('page')#获取请求参数
    try:
        activity=paginator.page(page)
    except PageNotAnInteger:
        activity=paginator.page(1)
    except InvalidPage:
        return HttpResponse("Bad Request")
    except EmptyPage:
        activity=paginator.page(paginator.num_pages)
    context['Activity']=activity#TODO：activity初值
    return render(request,"sua\\index.html",context)
class student(View):
    def get(self,request):
        Id=request.GET.get('id')
        username=request.GET.get('username')
        if (Id is not None):
            stu=StudentInfo.objects.get(id=int(Id))
            se=StudentInfo_Full_Serializer(instance=stu)
            return JsonResponse(se.data)
        elif (username is not None):
            stu=StudentInfo.objects.get(name=username)
            se=StudentInfo_Full_Serializer(instance=stu)
            return JsonResponse(se.data)
        else:
            stu=StudentInfo.objects.all()
            se=StudentInfo_Full_Serializer(instance=stu,many=True)
            return JsonResponse(se.data,safe=False)
    def post(self,request):
        pass     
class sua(View):
    def get(self,request):
        Id=request.GET.get('id')
        if (Id is not None):
            suas=Sua.objects.get(id=int(Id))
            se=Sua_Title_Serializer(instance=suas)
            return JsonResponse(se.data)
        else:
            suas=Sua.objects.all()
            se=Sua_Title_Serializer(instance=suas,many=True)
            return JsonResponse(se.data,safe=False)
    def post(self,request):
        pass
class activity(View):
    def get(self,request):
        Id=request.GET.get('id')
        if (Id is not None):
            ac=Activity.objects.get(id=int(Id))
            se=Activity_Full_Serializer(instance=ac)
            return JsonResponse(se.data)
        else:
            ac=Activity.objects.all()
            se=Activity_Title_Serializer(instance=suas,many=True)
            return JsonResponse(se.data,safe=False)
    def post(self,request):
        data=request.POST
        se=Activity_Full_Serializer(data=data)
        if (se.is_valid()):
            se.save()
            return HttpResponse("Good!")
        else:
            return JsonResponse(request.POST)



        


    
    
    
   
    
    
    
    
    