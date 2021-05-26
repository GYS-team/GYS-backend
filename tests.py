import os,django
import json
'''
此文件未完成。
'''
os.environ['DJANGO_SETTINGS_MODULE']='backend.settings'
django.setup()
from django.test import TestCase
from django.contrib.auth.models import User
from sua.views import ActivityView, ApplicationView, StudentView, SuaView
# Create your tests here.
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from sua.AdminViews import *
user = User.objects.get(username='19337001')
factory = APIRequestFactory()
f=open('test_result.txt','w')
def TestGET(url,view,**kwargs):
    f.write('GET ',url)
    request = factory.get(url,format='json')
    force_authenticate(request, user=user)
    response = view.as_view()(request,**kwargs)
    response.render()
    ans=json.loads(response.content)
    f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False),'\n')
def TestPOST(url,view,data):
    f.write('POST '+url)
    request = factory.post(url,data,format='json')
    force_authenticate(request, user=user)
    response = view.as_view()(request)
    response.render()
    ans=json.loads(response.content)
    f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
def run_all_TestGET():
    TestGET('/student/3',StudentView,id=3)
    TestGET('/student/admin/',AdminStudentView)
    TestGET('/activity/3',ActivityView,id=3)
    TestGET('/activity/admin/',AdminActivityView)
    TestGET('/sua/3',SuaView,id=3)
    TestGET('/sua/admin/',AdminSuaView)
    TestGET('/application/3',ApplicationView,id=3)
    TestGET('/application/admin/',AdminApplicationView)
def TestPUT(url,view,data):
    f.write('PUT '+url)
    request = factory.put(url,data,format='json')
    force_authenticate(request, user=user)
    response = view.as_view()(request)
    response.render()
    ans=json.loads(response.content)
    f.write(json.dumps(ans,indent=4, separators=(',', ':'), ensure_ascii=False)+'\n')
#run_all_TestGET()
ac_data={
    "title":"UTF8测试",
    "detail":"看看我能写多长，这么长差不多了吧",
    "is_valid":"false",
    "owner":8
}
#TestPOST('/activity/admin/',AdminActivityView,ac_data)
ac_data["id"]=11
ac_data["is_valid"]="true"
TestPUT('/activity/admin/',AdminActivityView,ac_data)
f.close()