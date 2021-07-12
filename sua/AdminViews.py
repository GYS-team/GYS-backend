from sua.BaseResponse.ResponseConst import CODE_PERMISSIONS_ERROR, MSG_PERMISSIONS_ERROR
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from .models import *
from .adminserializers import *
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import GenericAPIView
from .permissions import AdminPermissions,SuperAdminPermissions
from rest_framework.pagination import PageNumberPagination
from .BaseResponse import BaseResponse as BR
class AdminStudentView(GenericAPIView):
    permission_classes = [SuperAdminPermissions]
    #pagination_class=PageNumberPagination
    """
    get:
    请求返回所有学生信息。

    post:
    表示创建学生。user字段应传入一个字典，键是username（学号）和password。

    delete:
    根据学生编号删除学生。

    """
    queryset=StudentInfo.object.all()
    serializer_class=StudentInfoSerializer
    def get(self,request):
        if (request.GET.get('id',None)==None):
            se=self.get_serializer(instance=self.get_queryset(),many=True)
            return BR.BaseResponse(data=se.data)
        else:
            stu=self.get_queryset().filter(id=request.GET['id'])
            se=self.get_serializer(stu,many=True)
            return BR.BaseResponse(data=se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return BR.BaseResponse()
    def delete(self,request):
        Id=request.query_params['id']
        print(Id)
        stu=self.get_queryset().filter(id=Id)
        print(stu)
        stu.delete()
        return BR.BaseResponse()
    def put(self,request):        
        data=request.data
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)   
        if (se.is_valid(raise_exception=True)):
            se.save()        
        return BR.BaseResponse()

class AdminSuaView(GenericAPIView):
    permission_classes = [AdminPermissions]
    pagination_class=PageNumberPagination
    """
    get:
    请求返回所有sua信息。

    post:
    表示创建sua.

    delete:
    根据sua编号删除sua信息。

    """
    queryset=Sua.object.all()
    serializer_class=SuaSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.paginate_queryset(self.queryset),many=True)
        return self.get_paginated_response(se.data)
    def post(self,request):
        data=request.data.copy()
        
        if isinstance(data,list):
            for item in data:
                item['student']=User.objects.get(username=item['student']).studentinfo.id
            se=self.get_serializer(data=data,many=True)
            if (se.is_valid(raise_exception=True)):
                se.save()
                return BR.BaseResponse()
        if isinstance(data,dict):
            data['student']=User.objects.get(username=data['student']).studentinfo.id
            se=self.get_serializer(data=data)
            if (se.is_valid(raise_exception=True)):
                se.save()
                return BR.BaseResponse()
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return BR.BaseResponse()
    def put(self,request):
        #仅仅支持valid字段的修改
        data=request.data
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()
        return BR.BaseResponse()    

class AdminApplicationView(GenericAPIView):
    permission_classes = [SuperAdminPermissions]
    """
    get:
    请求返回所有申请信息。

    

    delete:
    根据申请编号删除申请信息。

    """
    queryset=Application.object.filter(is_checked=True)
    serializer_class=ApplicationSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return BR.BaseResponse(data=se.data)
    def put(self,request):
        data=request.data.copy()
        obj=self.get_queryset().get(id=data.pop('id'))
        
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()            
            if (obj.status==1 and obj.sua.added==False):                
                obj.sua.added=True                
                obj.owner.suahours+=obj.sua.suahours                
            if (obj.status==2 and obj.sua.added==True):
                obj.sua.added=False
                obj.owner.suahours-=obj.sua.suahours
                print(obj.owner.suahours)
            obj.owner.save()
            obj.sua.save()
            return BR.BaseResponse()


    
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().get(id=Id)
        stu.delete()
        return BR.BaseResponse()  
class AdminProofView(GenericAPIView):
    permission_classes = [SuperAdminPermissions]
    queryset=Proof.object.all()
    serializer_class=ProofSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.paginate_queryset(self.queryset),many=True)
        return self.get_paginated_response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return BR.BaseResponse(data={'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return BR.BaseResponse(data={'code':100,'msg':'Successfully deleted.'}) 
class AdminActivityView(GenericAPIView):
    permission_classes = [AdminPermissions]
    #pagination_class=PageNumberPagination
    """
    get:
    请求返回所有活动请信息。

    post:
    表示创建活动.

    delete:
    根据活动编号删除活动信息。
    
    put:
    根据活动编号和数据更改活动信息。
    """
    queryset=Activity.object.filter(is_created_by_admin=True)
    serializer_class=ActivitySerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        if (request.GET.get('id',None)!=None):
            id=request.query_params['id']
            suas=Activity.object.get(id=id).suas.all()
            se=SuaFullSerializer(instance=suas,many=True)
            return BR.BaseResponse(data=se.data)
        return BR.BaseResponse(data=se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)               
        if (se.is_valid(raise_exception=True)):
            se.save(owner=request.user.studentinfo)
            return BR.BaseResponse()
    def put(self,request):
        data=request.data
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()            
            if ((se.validated_data.get('is_valid',None)!=None) and request.user.studentinfo.power<2):
                return BR.BaseResponse(code=CODE_PERMISSIONS_ERROR,message=MSG_PERMISSIONS_ERROR) 
            if (obj.is_valid==True):
                for sua in obj.suas.all():
                    if (sua.added==False):
                        sua.added=True
                        sua.is_valid=True
                        sua.student.suahours+=sua.suahours
                        sua.save()
                        sua.student.save()
            if (obj.is_valid==False):
                for sua in obj.suas.all():
                    if (sua.added==True):
                        sua.added=False
                        sua.is_valid=False
                        sua.student.suahours-=sua.suahours
                        sua.save()
                        sua.student.save()
            return BR.BaseResponse()

    def delete(self,request):
        Id=request.query_params['id']
        print(Id)
        stu=self.get_queryset().filter(id=Id)
        print(stu)
        stu.delete()
        return BR.BaseResponse()  

class AdminChangePw(APIView):
    permission_classes=[SuperAdminPermissions]
    def post(self,request):
        new_pw=request.data['password']
        user=StudentInfo.object.get(id=request.data['id']).user
        user.set_password(new_pw)
        user.save()
        return BR.BaseResponse()

class AdminDeleteRecord(APIView):
    #todo
    def get(self,request):
        stu=StudentInfo.objects.filter(is_deleted=True)
        stu_se=StudentInfoSerializer(instance=stu,many=True)
        ac=Activity.objects.filter(is_deleted=True)
        print(ac)
        ac_se=ActivitySerializer(instance=ac,many=True)
        return BR.BaseResponse(data=[stu_se.data,ac_se.data])
