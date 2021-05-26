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
from rest_framework.permissions import IsAuthenticated
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
        se=self.get_serializer(data=data)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully created.'})
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})

class AdminApplicationView(GenericAPIView):
    permission_classes = [AdminPermissions]
    pagination_class=PageNumberPagination
    """
    get:
    请求返回所有申请信息。

    

    delete:
    根据申请编号删除申请信息。

    """
    queryset=Application.objects.all()
    serializer_class=ApplicationSerializer
    def get(self,request):
        se=self.get_serializer(instance=self.paginate_queryset(self.queryset),many=True)
        return self.get_paginated_response(se.data)
    
    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
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
    def put(self,request):
        data=request.data
        obj=self.get_queryset
        se=self.get_serializer(instance=obj,data=data,partial=True)
        if (se.is_valid(raise_exception=True)):
            se.save()
            return Response({'code':100,'msg':'Successfully updated.'})

    def delete(self,request):
        Id=request.query_params['id']
        stu=self.get_queryset().filter(id=Id)
        stu.delete()
        return Response({'code':100,'msg':'Successfully deleted.'})  
