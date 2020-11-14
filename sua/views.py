from django.shortcuts import render,HttpResponse,redirect
from .models import StudentInfo
# Create your views here.
def login(request):
    return render(request,"sua\\login.html")
def check(request):
    req=request.POST  #req is a dict    
    User_NetID=request.POST['NetID']
    User_PassWord=request.POST['PassWord']
    try:
        Correct_PassWord=StudentInfo.objects.get(NetID=User_NetID).PassWord
    except StudentInfo.DoesNotExist:
        return HttpResponse("用户不存在")
    if (Correct_PassWord==User_PassWord):         
        return redirect(index,User_NetID)         
    else:
        return HttpResponse("登录失败!")

    


    
    
    
   
    
    
    
    
    