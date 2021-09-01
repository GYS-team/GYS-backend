"""day1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.documentation import include_docs_urls
from . import AdminViews
from django.conf import settings
from django.conf.urls.static import static
authurl=[
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('changepassword/',views.ChangePw.as_view()),
]
studenturl=[
    
    path('index/',views.IndexView.as_view()),
    path('student/',views.StudentView.as_view()),
    path('sua/',views.SuaView.as_view()),
    path('activity/<int:id>',views.ActivityView.as_view()),    
    path('application/',views.ApplicationView.as_view()),      
    path('proof/',views.ProofView.as_view()),
]
adminurl=[path('student/admin/',AdminViews.AdminStudentView.as_view()),
    path('activity/admin/',AdminViews.AdminActivityView.as_view()),
    path('proof/admin/',AdminViews.AdminProofView.as_view()),
    path('sua/admin/',AdminViews.AdminSuaView.as_view()),
    path('application/admin/',AdminViews.AdminApplicationView.as_view()),
    path('changepw/admin/',AdminViews.AdminChangePw.as_view()),
    path('deleterecord/admin/',AdminViews.AdminDeleteRecord.as_view()),
    path('data/admin/',AdminViews.AdminData.as_view()),
]
    
urlpatterns = [
    #path('',views.Login,name='check'),
    #path('index/',views.index),
    #path('logout/',views.Logout,name='logout'),
    #path('changepassword/',views.changepassword,name='changepassword'),
    #path('applications/',views.applications,name='applications'),
    #以上是Django路由配置
    #以下是DRF路由配置
    #path('api-auth/', include('rest_framework.urls')),   
    path('docs/', include_docs_urls(title='文档')),
    path('export/',views.ExportView.as_view()),
]+authurl+studenturl+adminurl+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
