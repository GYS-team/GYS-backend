from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from .models import *
from .serializers import *
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
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
class Auth(APIView):
    def post(self,request):
        data=request.data 
        del data['Remember_me']#TODO
        if (data.pop('status')==0):
            se=UserSerializer(data=data)
            if (se.is_valid(raise_exception=True)):
                user = authenticate(**se.data)
                print(user)
                if (user is not None):   
                    login(request,user)
                    user.studentinfo.suahours=user.studentinfo.get_suahours()
                    return Response("Yes")       
                else:
                    return Response("No")
        else:
            logout(request)
            return Response("Yes")

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
class studentGenericAPIView(GenericAPIView):
    queryset=StudentInfo.objects.all()
    serializer_class=StudentInfo_Full_Serializer
    def get(self,request):
        Id=request.query_params.get('id')
        number=request.query_params.get('number')
        if (Id is not None):
            stu=StudentInfo.objects.get(id=Id)
            se= self.get_serializer(instance=stu)
            return Response(se.data)
        elif (number is not None):
            stu=StudentInfo.objects.get(number=number)
            se=self.get_serializer(instance=stu)
            return Response(se.data)
        else:
            stu=self.get_queryset()
            se=self.get_serializer(instance=stu,many=True)
            return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params.get('id')
        number=request.query_params.get('number')
        if (Id is not None):
            stu=StudentInfo.objects.get(id=int(Id))
            stu.delete()
            return Response({'code':100,'msg':'Successfully Deleted.'})
        elif (number is not None):
            stu=StudentInfo.objects.get(number=username)
            stu.delete()
            return Response({'code':100,'msg':'Successfully Deleted.'})
class sua(APIView):
    def get(self,request):
        Id=request.query_params.get('id')
        if (Id is not None):
            suas=Sua.objects.get(id=int(Id))
            se=Sua_Title_Serializer(instance=suas)
            return Response(se.data)
        else:
            suas=Sua.objects.all()
            se=Sua_Title_Serializer(instance=suas,many=True)
            return Response(se.data)
    def post(self,request):
        pass
class activity(APIView):
    def get(self,request):
        Id=request.query_params.get('id')
        if (Id is not None):
            ac=Activity.objects.get(id=int(Id))
            se=Activity_Full_Serializer(instance=ac)
            return Response(se.data)
        else:
            ac=Activity.objects.all()
            se=Activity_Full_Serializer(instance=ac,many=True)
            return Response(se.data)
    def post(self,request):
        data=request.data
        if (data.get('Id')==None):
            se=Activity_Full_Serializer(data=data,partial=True)
            if (se.is_valid(raise_exception=True)):
                se.save()
                return Response({'code':100,'msg':'Successfully created.'})
        elif (data.get('Id')!=None):
            instance=Activity.objects.get(id=data.pop('Id'))
            se=Activity_Full_Serializer(instance=instance,data=data,partial=True)
            if (se.is_valid(raise_exception=True)):
                se.save()
                return Response({'code':100,'msg':'Activity has been valid.'})
        



        


    
    
    
   
    
    
    
    
    