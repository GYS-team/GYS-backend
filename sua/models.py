from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Activity(models.Model):
    Time=models.IntegerField()
    def __str__(self):
        return str(self.Time)
class StudentInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    Activity=models.ForeignKey(Activity,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.user_id)
    
    
