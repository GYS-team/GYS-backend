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
urlpatterns = [
    #path('',views.Login,name='check'),
    #path('index/',views.index),
    #path('logout/',views.Logout,name='logout'),
    #path('changepassword/',views.changepassword,name='changepassword'),
    #path('applications/',views.applications,name='applications'),
    #以上是Django路由配置
    #以下是DRF路由配置
    #path('api-auth/', include('rest_framework.urls')),    
    path('student/<int:id>',views.StudentView.as_view()),
    path('student/admin/',views.AdminStudentView.as_view()),
    path('sua/<int:id>',views.SuaView.as_view()),
    path('sua/admin/',views.AdminSuaView.as_view()),
    path('activity/<int:id>',views.ActivityView.as_view()),
    path('activity/admin/',views.AdminActivityView.as_view()),
    path('auth/',views.Auth.as_view()),
    #path('admin/proof/',views.AdminProofView.as_view()),
    path('proof/<int:id>',views.ProofView.as_view()),
    #path('admin/application/',views.AdminApplicationView.as_view()),
    path('application/<int:id>',views.ApplicationView.as_view()),
   
]
