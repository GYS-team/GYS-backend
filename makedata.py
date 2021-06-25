
ActivityTitle=['Hello','Haha','Cool','Ohhhhh','God','fuck','gosh','goodbye','nmsl','goddamnit']
UserName=['ckh','cxc','dd','dzx','lhb','czm','abc','abc1','abc2']

PassWord=['123']
import os,django
os.system("del db.sqlite3")
os.system("del proofs/proofs")
os.system("cd sua")
os.environ['DJANGO_SETTINGS_MODULE']='backend.settings'
django.setup()
#每次开始时重置数据库
os.system("python manage.py makemigrations sua")
os.system("python manage.py migrate")
from django.contrib.auth.models import User
from sua.models import *
import random
def suahours_init():
    for i in range(len(UserName)):
        stu=User.objects.get(id=i+1).studentinfo
        stu.suahours=stu.get_suahours()
        stu.save()
for i in range(len(UserName)):
    user= User.objects.create_user(username=str(19337001+i),password='123')
    user.save()
print('successfully created %d Users.' % i)
for i in range(len(UserName)):
    stu=StudentInfo(user=User.objects.get(id=i+1),name=UserName[i],number=User.objects.get(id=i+1).username,power=2)
    stu.save()
print('successfully created %d StudentInfo.' % i)
count=0
for ac in ActivityTitle:
    count+=1
    activity=Activity(title=ac,owner=StudentInfo.object.get(id=random.randint(1,len(UserName))),is_valid=True)
    activity.save()
print('successfully created %d Activities.' % count)
count=0
for i in StudentInfo.object.all():
    for j in range(10):
        sua=Sua(student=i,activity=Activity.object.get(id=random.randint(1,len(ActivityTitle))),suahours=random.randint(1,10),is_valid=True,added=True)
        sua.save()
        count+=1
print('succesfully created %d suas'% count)
'''
for i in StudentInfo.object.all():
   proof=Proof.object.create(owner=i)
   proof.save()
   sua=Sua(student=i,activity=Activity.object.get(id=random.randint(1,len(ActivityTitle))),suahours=random.randint(1,10),is_valid=False)
   sua.save()
   application=Application.object.create(proof=proof,owner=i,sua=sua)
   application.save()
   proof=Proof.object.create(owner=i)
   proof.save()
'''
suahours_init()