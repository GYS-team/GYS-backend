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
        request.session['Is_Login']=True
        request.session['User_NetID']=User_NetID
        return redirect(index)         
    else:
        return HttpResponse("登录失败!")
def index(request):
    if (request.session['Is_Login']):
        NetID=request.session['User_NetID']
        try:
            context={'User_NetID':NetID,'Activity':StudentInfo.objects.get(NetID=NetID).Activity.Time}
        except AttributeError:
            context={'User_NetID':NetID,'Activity':'NULL'}
            
        return render(request,"sua\\index.html",context)
    else:
        return HttpResponse("No Permission")
def logout(request):
    request.session['Is_Login']=False
    return HttpResponse("退出登录成功!")
   
    


    
    
    
   
    
    
    
    
    