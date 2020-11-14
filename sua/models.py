from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Activity(models.Model):
    created = models.DateTimeField('创建日期', auto_now_add=True)
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=400)
    is_valid = models.BooleanField(default=False)
    def __str__(self):
        return self.title
class StudentInfo(models.Model):
    user = models.OneToOneField(
        User,#username:NetID 
        on_delete=models.CASCADE,
    )
    number=models.CharField(max_length=10)#学号
    suahours = models.FloatField(default=0)
    def get_suahours(self):
        total=0
        for sua in self.suas.all():
            total+=sua.suahours
        self.suahours=total
        self.save()
        return total
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Sua(models.Model):
    student = models.ForeignKey(
        StudentInfo,
        related_name='suas',
        on_delete=models.CASCADE,
    )
    activity = models.ForeignKey(
        Activity,
        related_name='suas',
        on_delete=models.CASCADE,
    )
    suahours = models.FloatField(default=0.0)
    
    
