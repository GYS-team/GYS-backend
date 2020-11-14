from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import StudentInfo
# Create your views here.
def Login(request):
    return render(request,"sua\\login.html")
def check(request):
    req=request.POST  #req is a dict    
    User_NetID=request.POST['NetID']
    User_Password=request.POST['Password']
    user = authenticate(username=User_NetID, password=User_Password)
    if (user is not None):   
        login(request,user)
        return redirect(index)         
    else:
        return HttpResponse("登录失败!")
@login_required
def index(request):
    NetID=request.user.username
    try:
        context={'User_NetID':NetID,'Activity':StudentInfo.objects.get(user=request.user).Activity.Time}
    except AttributeError:
        context={'User_NetID':NetID,'Activity':'NULL'}
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
        
    


    
    
    
   
    
    
    
    
    