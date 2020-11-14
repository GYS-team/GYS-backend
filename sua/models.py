from django.db import models

# Create your models here.
class Activity(models.Model):
    Time=models.IntegerField()
    def __str__(self):
        return str(self.Time)
class StudentInfo(models.Model):
    PassWord=models.CharField(max_length=20)
    NetID=models.CharField(max_length=20)
    Activity=models.ForeignKey(Activity,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.NetID
    
    
