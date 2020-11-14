from django.db import models

# Create your models here.

class StudentInfo(models.Model):
    PassWord=models.CharField(max_length=20)
    NetID=models.CharField(max_length=20)
    
    def __str__(self):
        return self.NetID
    
    
