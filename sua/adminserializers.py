from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username']
class UserFullSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    id=serializers.IntegerField(read_only=True)
class StudentInfoSerializer(serializers.ModelSerializer):
    user=UserFullSerializer()
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
        read_only_fields=['suahours']
    
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
        fields="__all__"
        extra_kwargs={
            "owner":{'help_text':'The organizer of activity,represented by his student_id'}
        }
        

class SuaSerializer(serializers.ModelSerializer):
    #student=StudentInfoSerializer()
    #activity=ActivitySerializer()
    class Meta:
        model=Sua
        fields="__all__"
    #Todo:update students' suahours when creating sua
class ProofSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proof
        fields="__all__"
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields="__all__"
       
class ActivityFullSerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
        fields=["created","title","detail"]

class SuaFullSerializer(serializers.ModelSerializer):
    activity=ActivityFullSerializer()
    class Meta:
        model=Sua
        fields=["activity","suahours"]
        
    