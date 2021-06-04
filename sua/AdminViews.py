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
from .permissions import AdminPermissions
from rest_framework.pagination import PageNumberPagination

class AdminStudentView(GenericAPIView):
    permission_classes = [AdminPermissions]
    #pagination_class=PageNumberPagination
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
        if (request.GET.get('id',None)==None):
            se=self.get_serializer(instance=self.get_queryset(),many=True)
            return Response(se.data)
        else:
            stu=self.get_queryset().filter(id=request.GET['id'])
            se=self.get_serializer(stu,many=True)
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
    def put(self,request):        
        data=request.data
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)   
        if (se.is_valid(raise_exception=True)):
            se.save()        
        return Response({'code':100,'msg':'Successfully updated.'})

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
    queryset=Sua.objects.all()
    serializer_class=SuaSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.paginate_queryset(self.queryset),many=True)
        return self.get_paginated_response(se.data)
    def post(self,request):
        data=request.data
        if isinstance(data,list):
            se=self.get_serializer(data=data,many=True)
            if (se.is_valid(raise_exception=True)):
                se.save()
                return Response({'code':100,'msg':'Successfully created.'})
        if isinstance(data,dict):
            se=self.get_serializer(data=data)
            if (se.is_valid(raise_exception=True)):
                se.save()
                return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})
    def put(self,request):
        data=request.data
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()
        return Response({'code':100,'msg':'Successfully updated.'})    

class AdminApplicationView(GenericAPIView):
    permission_classes = [AdminPermissions]
    """
    get:
    请求返回所有申请信息。

    

    delete:
    根据申请编号删除申请信息。

    """
    queryset=Application.objects.filter(is_checked=True)
    serializer_class=ApplicationSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def put(self,request):
        data=request.data.copy()
        obj=self.get_queryset().get(id=data.pop('id'))
        if (obj.status!=0):
            return Response({'code':200,'msg':'No Permissions'})
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
            return Response({'code':100,'msg':'Successfully updated.'})


    
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().get(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})  
class AdminProofView(GenericAPIView):
    permission_classes = [AdminPermissions]
    """
    待更新，因为涉及文件传输问题。
    """
    queryset=Proof.objects.all()
    serializer_class=ProofSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.paginate_queryset(self.queryset),many=True)
        return self.get_paginated_response(se.data)
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
    queryset=Activity.objects.filter(is_created_by_admin=True)
    serializer_class=ActivitySerializer
    def get(self,request):
        se=self.get_serializer(instance=self.get_queryset(),many=True)
        return Response(se.data)
    def post(self,request):
        data=request.data
        se=self.get_serializer(data=data)               
        if (se.is_valid(raise_exception=True)):
            se.save(owner=request.user.studentinfo)
            return Response({'code':100,'msg':'Successfully created.'})
    def put(self,request):
        data=request.data
        obj=self.get_queryset().get(id=data.pop('id'))
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()
            if (se.is_valid(raise_exception=True)):
                print(obj.is_valid)
                if (obj.is_valid==True):
                    for sua in obj.suas.all():
                        if (sua.added==False):
                            sua.added=True
                            sua.is_valid=True
                            sua.student.suahours+=sua.suahours
                            sua.save()
                            sua.student.save()
                if (obj.is_valid==False):
                    for sua in obj.sua.all():
                        if (sua.added==True):
                            sua.added=False
                            sua.is_valid=False
                            sua.student.suahours+=sua.suahours
                            sua.save()
                            sua.student.save()
            return Response({'code':100,'msg':'Successfully updated.'})

    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})  

class AdminChangePw(APIView):
    kpermission_classes=[AdminPermissions]
    def post(self,request):
        new_pw=request.data['password']
        user=StudentInfo.objects.get(id=request.data['id']).user
        user.set_password(new_pw)
        user.save()
        return Response('{result:1}')