#coding=utf8
import json
import django

import os
'''
此文件未完成。
'''
os.environ['DJANGO_SETTINGS_MODULE']='backend.settings'
django.setup()
os.system("python makedata.py")
from django.test import TestCase
from django.contrib.auth.models import User
from sua.views import *
from sua.AdminViews import *
# Create your tests here.
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from sua.AdminViews import *
class Test():
    def __init__(self,username):
        self.user= User.objects.get(username=username)
        self.factory = APIRequestFactory()
        self.f=open('test_result.txt','a+')
        print('#')
    def TestGET(self,url,view,**kwargs):
        self.f.write('GET '+url)
        os.system('tail test_result.txt')
        request = self.factory.get(url,format='json')
        force_authenticate(request, user=self.user)
        response = view.as_view()(request,**kwargs)
        response.render()
        ans=json.loads(response.content)
        
        self.f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
    def TestPOST(self,url,view,data):
        self.f.write('POST '+url)
        request = self.factory.post(url,data,format='json')
        force_authenticate(request, user=self.user)
        response = view.as_view()(request)
        response.render()
        ans=json.loads(response.content)
        self.f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
    def TestPUT(self,url,view,data):
        self.f.write('PUT '+url)
        request = self.factory.put(url,data,format='json')
        force_authenticate(request, user=self.user)
        response = view.as_view()(request)
        response.render()
        ans=json.loads(response.content)
        self.f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
    def run_test(self):    
        
        self.TestGET('student/',StudentView)
        self.TestGET('index/',IndexView)
        app_data={
            "proof": {
                "is_offline": "true",
            },
            "sua": {
                "activity": {
                    "title": "testing",
                    "detail": "100个公益时"
                },
                "suahours": 100.0
            },
            "contact": "13612687802",
            "is_checked": "true",
        }
        self.TestPOST('application/',ApplicationView,app_data)
        self.TestGET('application/',ApplicationView)
        app_data['id']=1
        app_data['contact']="136"
        self.TestPUT('application/',ApplicationView,app_data)
        #学生端通过上述操作提交并修改过申请
        #管理员通过以下手段审查
        self.f.write('申请已提交\n')
        self.TestGET('application/admin/',AdminApplicationView)
        self.TestPUT('application/admin/',AdminApplicationView,{'id':1,"status":1})
        #管理员审查通过
        self.f.write('申请已通过')
        self.TestGET('student/',StudentView)
        #管理员修改审查结果
        self.TestPUT('application/admin/',AdminApplicationView,{'id':1,"status":2})
        self.f.write("管理员把结果改为申请失败")
        self.TestGET('student/',StudentView)
        #以下是管理员端口的测试
        
        self.TestGET('student/admin/',AdminStudentView)
        print('1')
        #管理员创建活动
        ac_data={
            "title":"测试端测试",
            "detail":"测试"
        }
        self.TestPOST('activity/admin/',AdminActivityView,ac_data)
        print('2')
        self.TestGET('activity/admin/',AdminActivityView)
        ac_data['title']="我改过了"
        ac_data['id']=12 #注意前面添加过一个活动了，而且管理员无权修改非管理员创建的活动
        self.TestPUT('activity/admin/',AdminActivityView,ac_data)
        self.TestGET('activity/admin/',AdminActivityView)
        
        sua_data=[{"student":"19337001","suahours":"500","activity":"12"},{"student":"19337002","activity":"12"}]
        self.TestPOST('sua/admin/',AdminSuaView,sua_data)
        ac_data['is_valid']="true"
        self.TestPUT('activity/admin',AdminActivityView,ac_data)
        self.TestGET('activity/admin/?id=12',AdminActivityView)
        self.f.write('管理员审核活动通过')
        self.TestGET('student/admin/',AdminStudentView)
        self.f.write('管理员让活动不通过')
        ac_data['is_valid']="false"
        self.TestPUT('activity/admin/',AdminActivityView,ac_data)
        self.TestGET('student/admin/',AdminStudentView)
        self.f.close()
        
print('test')
all_api_test=Test(username='19337003')
all_api_test.run_test()
Permissions_test=Test(username='19337002')





