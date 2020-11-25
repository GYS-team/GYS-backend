from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from .models import StudentInfo
# Create your views here.
def Login(request):
    return render(request,"sua\\login.html")
def check(request):
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


    


    
    
    
   
    
    
    
    
    