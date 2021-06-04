from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .storage import FileStorage
import datetime
YEAR_CHOICES = []
for r in range(2016, datetime.datetime.now().year+1):
    YEAR_CHOICES.append((r, r))
# Create your models here.
class StudentInfo(models.Model):
    user = models.OneToOneField(
        User,  
        on_delete=models.CASCADE,
    )
    number = models.CharField(max_length=10)  # 学号
    suahours = models.FloatField(default=0)
    classtype = models.CharField(max_length=100,default='一班')
    grade = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year
    )
    phone = models.CharField(max_length=100,default='000')
    power = models.IntegerField(default=0)  
    name = models.CharField(max_length=100)
    def get_suahours(self):
        total = 0
        for sua in self.suas.all():
            if (sua.is_valid is True):
                total += sua.suahours
        self.suahours = total
        self.save()
        return total

    

    def __str__(self):
        return self.name
class Activity(models.Model):
    owner=models.ForeignKey(
        StudentInfo,
        related_name="activity",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('创建日期', auto_now=True)
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=400)
    is_valid = models.BooleanField(default=False)
    is_created_by_admin=models.BooleanField(default=False)
    def __str__(self):
        return self.title





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
    is_valid=models.BooleanField(default=False)
    added=models.BooleanField(default=False)


class Proof(models.Model):
    owner = models.ForeignKey(
        StudentInfo,
        related_name='proofs',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    is_offline = models.BooleanField(default=False)
    proof_file = models.FileField(
        upload_to='proofs',
        storage=FileStorage(),
        blank=True,
    )

    


class Application(models.Model):
    sua = models.OneToOneField(
        Sua,
        related_name='application',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        StudentInfo,
        related_name='applications',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('创建日期', default=timezone.now)
    contact = models.CharField(max_length=100, blank=True) #联系方式
    proof = models.OneToOneField(
        Proof,
        related_name='applications',
        on_delete=models.CASCADE,
    )
    is_checked = models.BooleanField(default=False) #是否已经由owner提交
    status = models.IntegerField(default=0)  # 0: 待审核，1：通过 2：不通过
    feedback = models.CharField(max_length=400, blank=True)
   

    def __str__(self):
        return self.sua.student.name + '的 ' + self.sua.activity.title + '的 ' + '申请'
