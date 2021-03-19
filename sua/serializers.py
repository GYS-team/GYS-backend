from rest_framework import serializers
from .models import *
class UserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=10)
    password=serializers.CharField(max_length=100,write_only=True)
    def create(self,validated_data):
        new_user=User.objects.create(**validated_data)
        return new_user
class StudentInfo_Full_Serializer(serializers.Serializer):
    number=serializers.CharField(max_length=10)
    suahours = serializers.FloatField(default=0) 
    user=UserSerializer(write_only=True)  
    def create(self,validated_data):
        new_user=User.objects.create(validated_data.pop("user"))
        new_stu=StudentInfo.objects.create(user=new_user,**validated_data)
        return new_stu
class StudentInfo_Short_Serializer(serializers.Serializer):
    number=serializers.CharField(max_length=10)
    name=serializers.CharField(max_length=100,read_only=True)
class Activity_Full_Serializer(serializers.Serializer):
    owner=StudentInfo_Short_Serializer()
    created=serializers.DateTimeField(read_only=True)
    title = serializers.CharField(max_length=100)
    detail = serializers.CharField(max_length=400)
    is_valid = serializers.BooleanField(default=False)
    def create(self,validated_data):
        stu=StudentInfo.objects.get(number=validated_data.pop("number"))
        new_ac=Activity.objects.create(owner=stu,**validated_data)
        return new_ac
    def update(self,instance,validated_data):
        instance.title=validated_data.get('title')
        instance.detail=validated_data.get('detail')
        instance.is_valid=validated_data.get('is_valid')
        instance.save()
        return instance


class Activity_Title_Serializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    is_valid=serializers.BooleanField(default=False)
class Sua_Full_Serializer(serializers.Serializer):
    student=StudentInfo_Full_Serializer()
    activity=Activity_Title_Serializer()
    suahours = serializers.FloatField(default=0.0)
        
        
    
    