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
        new_stu=StudentInfo.object.create(user=new_user,**validated_data)
        return new_stu
        
            
    class Meta:
        model=StudentInfo   
        exclude=["is_deleted","deleted_at"]
        extra_kwargs={
            "user":{'help_text':'student对象对应的user对象'},
            "name":{'help_text':'学生姓名'},
            "number":{'help_text':'学号'}
        }
        read_only_fields=['suahours']

class StudentInfoBasicSerializer(serializers.ModelSerializer):
        
     class Meta:
         model=StudentInfo
         fields=['user','name','id']
         read_only_fields=['user','name','id']
class ActivitySerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        owner=validated_data.pop('owner')
        new_ac=Activity.object.create(owner=owner,is_created_by_admin=True,**validated_data)
        return new_ac
    class Meta:
        model=Activity
        exclude=["is_deleted","deleted_at"]
        extra_kwargs={
            "owner":{'help_text':'The organizer of activity,represented by his student_id'}
        }
        read_only_fields=['is_created_by_admin','owner']


class SuaSerializer(serializers.ModelSerializer):
    #student=StudentInfoBasicSerializer()
    #activity=ActivitySerializer()

    class Meta:
        model=Sua
        exclude=["is_deleted","deleted_at"]


class ProofSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proof
        exclude=["is_deleted","deleted_at"]
class SuaBasicSerializer(serializers.ModelSerializer):
    #activty查sua用
    student=StudentInfoBasicSerializer()
    class Meta:
        model=Sua
        fields=["student","suahours"]
class SuaFullSerializer(serializers.ModelSerializer):
    student=StudentInfoBasicSerializer()
    activity=ActivitySerializer()
    class Meta:
        model=Sua
        fields=["student","activity","suahours"]
class ApplicationSerializer(serializers.ModelSerializer):
    proof=ProofSerializer()
    sua=SuaFullSerializer()
    class Meta:
        model=Application
        exclude=["is_deleted","deleted_at"]
        read_only_fields=['sua','owner','proof','contact','is_checked','created']   


    