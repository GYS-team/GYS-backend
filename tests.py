import os,django
import json
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
user = User.objects.get(username='19337001')
factory = APIRequestFactory()
f=open('test_result.txt','w')
def TestGET(url,view,**kwargs):
    f.write('GET '+url)
    request = factory.get(url,format='json')
    force_authenticate(request, user=user)
    response = view.as_view()(request,**kwargs)
    response.render()
    ans=json.loads(response.content)
    f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
def TestPOST(url,view,data):
    f.write('POST '+url)
    request = factory.post(url,data,format='json')
    force_authenticate(request, user=user)
    response = view.as_view()(request)
    response.render()
    ans=json.loads(response.content)
    f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
def TestPUT(url,view,data):
    f.write('PUT '+url)
    request = factory.put(url,data,format='json')
    force_authenticate(request, user=user)
    response = view.as_view()(request)
    response.render()
    ans=json.loads(response.content)
    f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
def run_test():
    TestGET('student/',StudentView)
    TestGET('index/',IndexView)
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
    TestPOST('application/',ApplicationView,app_data)
    TestGET('application/',ApplicationView)
    app_data['id']=1
    app_data['contact']="136"
    TestPUT('application/',ApplicationView,app_data)
    #学生端通过上述操作提交并修改过申请
    #管理员通过以下手段审查
    f.write('申请已提交\n')
    TestGET('application/admin/',AdminApplicationView)
    TestPUT('application/admin/',AdminApplicationView,{'id':1,"status":1})
    #管理员审查通过
    f.write('申请已通过')
    TestGET('student/',StudentView)
    #管理员修改审查结果
    TestPUT('application/admin/',AdminApplicationView,{'id':1,"status":2})
    f.write("管理员把结果改为申请失败")
    TestGET('student/',StudentView)
    #以下是管理员端口的测试
    TestGET('student/admin/',AdminStudentView)
    #管理员创建活动
    ac_data={
        "title":"测试端测试",
        "detail":"测试"
    }
    TestPOST('activity/admin/',AdminActivityView,ac_data)
    TestGET('activity/admin/',AdminActivityView)
    ac_data['title']="我改过了"
    ac_data['id']=12 #注意前面添加过一个活动了，而且管理员无权修改非管理员创建的活动
    TestPUT('activity/admin/',AdminActivityView,ac_data)
    TestGET('activity/admin/',AdminActivityView)
    sua_data=[{"student":"19337001","suahours":"500","activity":"12"},{"student":"19337002","activity":"12"}]
    TestPOST('sua/admin/',AdminSuaView,sua_data)
    ac_data['is_valid']="true"
    TestPUT('activity/admin',AdminActivityView,ac_data)
    TestGET('activity/admin/?id=12',AdminActivityView)
    f.write('管理员审核活动通过')
    TestGET('student/admin/',AdminStudentView)
run_test()
f.close()
