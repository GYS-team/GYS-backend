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
    """
    post:
    登录认证。
    发送的Post请求应该具有如下格式：
    {
        'status':0,
        'Remember_me':'True',
        'username':'19337001',
        'password':'123'
    }
    如果验证成功将返回：
    {
        'result':1,
        'id':学生编号
    }
    如果验证失败将返回：
    {
        'result':0
    }
    或者：
    {
        'status':1,
    }
    表示退出登录。

    """
    def post(self,request):
        data=request.data 
        del data['Remember_me']#TODO
        if (int(data.pop('status'))==0):
            se=UserSerializer(data=data)
            if (se.is_valid(raise_exception=True)):
                user = authenticate(**se.validated_data)
                if (user is not None):   
                    login(request,user)
                    user.studentinfo.suahours=user.studentinfo.get_suahours()
                    return Response({'result':1,'id':user.studentinfo.id})       
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
    """
    
    通过学生编号查询学生信息。
    """
    queryset=StudentInfo.objects.all()
    serializer_class=StudentInfoSerializer
    lookup_field='id'
    def get(self,request,id):
        stu=self.get_object()
        se= self.get_serializer(instance=stu)
        return Response(se.data)    
class AdminStudentView(GenericAPIView):
    """
    get:
    请求返回所有学生信息。

    post:
    表示创建学生。user字段应传入一个字典，键是username（学号）和password。

    delete:
    根据学生编号删除学生。

    """
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
    """
    
    通过sua编号查询sua信息。
    """
    queryset=Sua.objects.all()
    serializer_class=SuaSerializer
    lookup_field='id'
    def get(self,request,id):
        sua=self.get_object()
        se= self.get_serializer(instance=sua)
        return Response(se.data) 
class AdminSuaView(GenericAPIView):
    """
    get:
    请求返回所有sua信息。

    post:
    表示创建sua.

    delete:
    根据sua编号删除sua信息。

    """
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
    """
    
    通过活动编号查询活动信息。
    """
    queryset=Activity.objects.all()
    serializer_class=ActivitySerializer
    lookup_field='id'
    def get(self,request,id):
        ac=self.get_object()
        se= self.get_serializer(instance=ac)
        return Response(se.data) 
    
class AdminActivityView(GenericAPIView):
    """
    get:
    请求返回所有活动请信息。

    post:
    表示创建活动.

    delete:
    根据活动编号删除活动信息。

    """
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
    """
    待更新，因为涉及文件传输问题。
    """
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
    """
    待更新，涉及文件传输问题。
    """
    queryset=Proof.objects.all()
    serializer_class=ProofSerializer
    lookup_field='id'
    def get(self,request,id):
        ac=self.get_object()
        se= self.get_serializer(instance=ac)
        return Response(se.data) 

class ApplicationView(GenericAPIView):
    """
    get:
    通过申请编号查询申请信息。

    """
    queryset=Application.objects.all()
    serializer_class=ApplicationSerializer
    lookup_field='id'
    def get(self,request,id):
        ac=self.get_object()
        se= self.get_serializer(instance=ac)
        return Response(se.data) 
    
class AdminApplicationView(GenericAPIView):
    """
    get:
    请求返回所有申请信息。

    post:
    表示创建申请.

    delete:
    根据申请编号删除申请信息。

    """
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
   
class IndexView(APIView):
    """
    id是指学生编号。
    这时返回的是学生的所有sua信息，足够展示其个人主页。
    """
    def get(self,request,id):
        sua=StudentInfo.objects.get(id=id).suas.all()
        se=SuaFullSerializer(instance=sua,many=True)
        return Response(se.data)   
    
    
    
    