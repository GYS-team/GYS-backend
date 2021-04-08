from rest_framework import serializers
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username']
class StudentInfoSerializer(serializers.ModelSerializer):
    #def create(self,validated_data):
    #    new_user=User.objects.create(**validated_data.pop("user"))
     #   new_stu=StudentInfo.objects.create(user=new_user,**validated_data)
     #   return new_stu
    class Meta:
        model=StudentInfo   
        fields="__all__"
    
class ActivitySerializer(serializers.ModelSerializer):
    #def create(self,validated_data):
    #    stu=StudentInfo.objects.get(number=validated_data.pop("owner")['number'])
     #   new_ac=Activity.objects.create(owner=stu,**validated_data)
     #   return new_ac
    def update(self,instance,validated_data):
        instance.title=validated_data.get('title')
        instance.detail=validated_data.get('detail')
        instance.is_valid=validated_data.get('is_valid')
        instance.save()
        return instance
    #owner=StudentInfoSerializer()
    class Meta:
        model=Activity
        fields="__all__"

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
       
    
    