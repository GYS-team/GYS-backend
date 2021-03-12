from rest_framework import serializers
from .models import *
class UserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=10)
    #password=serializers.CharField(max_length=100)
class StudentInfo_Full_Serializer(serializers.Serializer):
    number=serializers.CharField(max_length=10)
    suahours = serializers.FloatField(default=0)
    name = serializers.CharField(max_length=100)
    user=UserSerializer()
class Activity_Full_Serializer(serializers.Serializer):
    created=serializers.DateTimeField(read_only=True)
    title = serializers.CharField(max_length=100)
    detail = serializers.CharField(max_length=400)
    is_valid = serializers.BooleanField(default=False)
    def create(self,validated_data):
        ac=Activity.objects.create(**validated_data)
        return ac
class StudentInfoSerializer(serializers.ModelSerializer):
    #mobile=serializers.CharField(max_length=400)
    class Meta:
        model=StudentInfo
        fields="__all__"
        
        
    
    