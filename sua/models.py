from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


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
        User,  # username:NetID
        on_delete=models.CASCADE,
    )
    number = models.CharField(max_length=10)  # 学号
    suahours = models.FloatField(default=0)

    def get_suahours(self):
        total = 0
        for sua in self.suas.all():
            total += sua.suahours
        self.suahours = total
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


class Proof(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='proofs',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    is_offline = models.BooleanField(default=False)
    proof_file = models.FileField(
        upload_to='proofs',
        blank=True,
    )


class Application(models.Model):
    sua = models.OneToOneField(
        Sua,
        related_name='application',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        User,
        related_name='applications',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField('创建日期', default=timezone.now)
    proof = models.ForeignKey(
        Proof,
        related_name='applications',
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(default=0)  # 0: 通过; 1: 未通过; 2: 需要线下证明
    feedback = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.sua.student.name + '的 ' + self.sua.activity.title + '的 ' + '申请'
