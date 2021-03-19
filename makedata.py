ActivityTitle=['Hello','Haha','Cool','Ohhhhh','God','fuck','gosh','goodbye','nmsl','goddamnit']
UserName=['ckh','cxc','dd','dzx','lhb','czm','abc','abc1','abc2']
import os,django
PassWord=['123']
#由于以下代码需要在Django Shell中运行，因此初始配置：
os.environ['DJANGO_SETTINGS_MODULE']='backend.settings'
django.setup()
from django.contrib.auth.models import User
from sua.models import *
import random
#每次开始时重置数据库
os.system("python manage.py makemigrations sua")
os.system("python manage.py migrate")
for us in UserName:
    user= User.objects.create_user(username=us,password='123')
    user.save()
for i in range(len(UserName)):
    stu=StudentInfo(user=User.objects.get(id=i+1),name=User.objects.get(id=i+1).username,number=19337000+i)
    stu.save()
for ac in ActivityTitle:
    activity=Activity(title=ac,owner=StudentInfo.objects.get(id=random.randint(1,len(UserName))))
    activity.save()
for i in StudentInfo.objects.all():
    for j in range(50):
        sua=Sua(student=i,activity=Activity.objects.get(id=random.randint(1,len(ActivityTitle))),suahours=random.randint(1,10))
        sua.save()
    
    