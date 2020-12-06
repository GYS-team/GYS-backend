from .models import Activity,StudentInfo,Sua
from rest_framework import serializers
from django.contrib.auth.models import User
class ActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model=Activity
        fields=('created','title','detail','is_valid')
class StudentInfoSerializers(serializers.ModelSerializer):    
    class Meta:
        model=StudentInfo
        fields=('user','number','name','suahours','suas')    
class SuaSerializers(serializers.ModelSerializer):
    activity=ActivitySerializers()
    student=StudentInfoSerializers()
    stuhours=serializers.FloatField(default=0.0)
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password')

        