from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username']
class UserFullSerializer(serializers.Serializer):
    #登录认证用
    username=serializers.CharField()
    password=serializers.CharField()
class StudentInfoSerializer(serializers.ModelSerializer):
    # 展示个人主页的信息用
    user=UserFullSerializer(write_only=True)
    def create(self,validated_data):
        new_user=User.objects.create(**validated_data.pop("user"))
        new_stu=StudentInfo.objects.create(user=new_user,**validated_data)
        return new_stu
    class Meta:
        model=StudentInfo   
        fields="__all__"
        extra_kwargs={
            "user":{'help_text':'student对象对应的user对象'},
            "name":{'help_text':'学生姓名'},
            "number":{'help_text':'学号'}
        }
    
class ActivitySerializer(serializers.ModelSerializer):
    #展示活动详情用
    class Meta:
        model=Activity
        exclude=["owner","is_valid"]

class SuaSerializer(serializers.ModelSerializer):
    activity=ActivitySerializer()
    #给application用的
    class Meta:
        model=Sua
        exclude=['is_valid','student']
    #Todo:update students' suahours when creating sua
class ProofSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proof
        exclude=['owner']
        
class ApplicationSerializer(serializers.ModelSerializer):
    #查询申请
    sua=SuaSerializer()
    proof=ProofSerializer()
    def create(self,validated_data):
        ac_data=validated_data['sua']['activity']
        sua_data=validated_data['sua']
        del sua_data['activity']
        stu=validated_data.pop('stu')
        new_ac=Activity.objects.create(**ac_data,owner=stu)
        new_sua=Sua.objects.create(**sua_data,activity=new_ac,student=stu)
        del validated_data['sua']
        app_data=validated_data
        new_pf=Proof.objects.create(owner=stu,**validated_data.pop('proof'))
        new_pf.save()
        new_app=Application.objects.create(**app_data,sua=new_sua,owner=stu,proof=new_pf)
        new_app.save()
        new_ac.save()
        new_sua.save()
        return new_app
    class Meta:
        model=Application
        exclude=["owner"]
        read_only_fields=["status","feedback"]
       


class SuaFullSerializer(serializers.ModelSerializer):
    #展示个人主页的公益时信息用
    activity=ActivitySerializer()
    class Meta:
        model=Sua
        fields=["activity","suahours"]
        
    