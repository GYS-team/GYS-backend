from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from .models import *
from .studentserializers import *
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .permissions import ActivityPermissions, AdminPermissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

#以上是Django的视图函数
#以下是DRF的视图函数 


class LoginView(ObtainAuthToken):
    """
    post:
    登录认证。
    发送的Post请求应该具有如下格式：
    {
        'username':'19337001',
        'password':'123'
    }
    如果验证成功将返回：
    {
        'result':1,
        'id':学生编号
        'token':token
    }
    如果验证失败将返回：
    {
        'result':0
    }
   
    """
    def post(self,request):
        data=request.data 
        se=UserFullSerializer(data=data)
        if (se.is_valid(raise_exception=True)):
            user = authenticate(**se.validated_data)
            if (user is not None):   
                Token.objects.filter(user=user).delete()
                token, created = Token.objects.get_or_create(user=user)
                user.studentinfo.suahours=user.studentinfo.get_suahours()
                return Response({'result':1,'id':user.studentinfo.id,'token':token.key})       
            else:
                return Response({'result':0})
        
class LogoutView(APIView):
    queryset = User.objects.all()    
    def get(self, request):
        ret={}
        try:
            # 退出时删除用户登录时生成的Token
            Token.objects.filter(user=request.user).delete()
            ret['result'] = 1
        except Exception as e:
            ret['result']= 0
        return Response(ret)
class ChangePw(APIView):
    '''
    post:
    只需提交password字段即可。
    '''
    permission_classes=[IsAuthenticated]
    def post(self,request):
        new_pw=request.data['password']
        user=request.user
        user.set_password(new_pw)
        user.save()
        return Response('{result:1}')
class StudentView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    """
    
    通过学生编号查询学生信息。
    """
    serializer_class=StudentInfoSerializer
    def get(self,request):
        stu=StudentInfo.objects.get(id=request.user.studentinfo.id)
        se= self.get_serializer(instance=stu)
        return Response(se.data)    

class ActivityView(GenericAPIView):
    permission_classes=[IsAuthenticated,ActivityPermissions]
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



class ApplicationView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    """
    get:
    通过申请编号查询申请信息。
    post:
    创建新申请
    """    
    queryset=Application.objects.all()
    serializer_class=ApplicationSerializer
    def get(self,request):
        query=Application.objects.filter(owner=request.user.studentinfo)
        se= self.get_serializer(instance=query,many=True)
        return Response(se.data) 
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save(stu=request.user.studentinfo)
            return Response({'code':100,'msg':'Successfully created.'})
    def put(self,request):
        data=request.data.copy()
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()
        return Response({'code':100,'msg':'Successfully updated.'})
class ProofView(GenericAPIView):
    '''
    post:
    提交证明文件。只支持html form表单提交。
    '''
    permission_classes=[IsAuthenticated]
    serializer_class=ProofSerializer
    def post(self,request):
        stu=StudentInfo.objects.get(id=1)
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save(owner=stu)
        return Response({'code':'100','msg':'successfully created'})
class IndexView(APIView):
    permission_classes=[IsAuthenticated]
    '''
    get:
    这时返回的是学生的所有sua信息，足够展示其个人主页。
    '''
    def get(self,request):
        sua=StudentInfo.objects.get(id=request.user.studentinfo.id).suas.all()
        se=SuaFullSerializer(instance=sua,many=True)
        return Response(se.data)   
    
    
# 以下仅作代码备份用
class SuaView(GenericAPIView):
    permission_classes=[IsAuthenticated]
    """
    
    通过sua编号查询sua信息。
    此API已弃用，仅作备份。
    """
    queryset=Sua.objects.all()
    serializer_class=SuaSerializer
    lookup_field='id'
    def get(self,request,id):
        sua=self.get_object()
        se= self.get_serializer(instance=sua)
        return Response(se.data) 
    