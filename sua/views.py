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
        print(data)
        del data['Remember_me']#TODO
        if (int(data.pop('status'))==0):
            se=UserSerializer(data=data)
            if (se.is_valid(raise_exception=True)):
                print(se.data)
                user = authenticate(**se. validated_data)
                if (user is not None):   
                    print("Yes")
                    login(request,user)
                    user.studentinfo.suahours=user.studentinfo.get_suahours()
                    return Response({'result':1,'id':user.id})       
                else:
                    return Response({'result':0})
        else:
            logout(request)
            return Response({'result':1})

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
class StudentView(GenericAPIView):
    queryset=StudentInfo.objects.all()
    serializer_class=StudentInfoSerializer
    lookup_field='id'
    def get(self,request,id):
        stu=self.get_object()
        se= self.get_serializer(instance=stu)
        return Response(se.data)    
class AdminStudentView(GenericAPIView):
    queryset=StudentInfo.objects.all()
    serializer_class=StudentInfoSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})

class SuaView(GenericAPIView):
    queryset=Sua.objects.all()
    serializer_class=SuaSerializer
    lookup_field='id'
    def get(self,request,id):
        sua=self.get_object()
        se= self.get_serializer(instance=sua)
        return Response(se.data) 
class AdminSuaView(GenericAPIView):
    queryset=Sua.objects.all()
    serializer_class=SuaSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})
class ActivityView(GenericAPIView):
    queryset=Activity.objects.all()
    serializer_class=ActivitySerializer
    lookup_field='id'
    def get(self,request,id):
        ac=self.get_object()
        se= self.get_serializer(instance=ac)
        return Response(se.data) 
    
class AdminActivityView(GenericAPIView):
    queryset=Activity.objects.all()
    serializer_class=ActivitySerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})  

class AdminProofView(GenericAPIView):
    queryset=Proof.objects.all()
    serializer_class=ProofSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'}) 

class ProofView(GenericAPIView):  
    queryset=Proof.objects.all()
    serializer_class=ProofSerializer
    lookup_field='id'
    def get(self,request,id):
        ac=self.get_object()
        se= self.get_serializer(instance=ac)
        return Response(se.data) 

class ApplicationView(GenericAPIView):
    queryset=Application.objects.all()
    serializer_class=ApplicationSerializer
    lookup_field='id'
    def get(self,request,id):
        ac=self.get_object()
        se= self.get_serializer(instance=ac)
        return Response(se.data) 
    
class AdminApplicationView(GenericAPIView):
    queryset=Application.objects.all()
    serializer_class=ApplicationSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})  
   
    
    
    
    
    