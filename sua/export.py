from .studentserializers import *
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import *
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
import os
from reportlab.pdfbase.ttfonts import TTFont
def Download(request):

    pdfmetrics.registerFont(TTFont('song', os.getcwd() + '/sua/STSONG.ttf'))
    user = request.user
    student = user.studentinfo
    sua_data = SuaSerializer(  # 序列化当前学生的所有公益时记录
                student.suas.filter(is_valid=True,activity__is_valid=True),
                many=True)


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=公益时'

    buffer = BytesIO()
    zuo = 50
    kuan = 210
    you = 545
    p = canvas.Canvas(buffer)

    p.filename = student.name

    p.setFont("song", 22)#字号
    p.drawString(zuo-5,780,"公益时记录",)#标题
    #p.drawImage('project/sua/static/sua/images/logo-icon.png',460,705,width=90,height=90)#学院标志
    p.setFont("song", 15) #字号
    p.drawString(zuo-5,750,'学号:'+str(user))#学号
    p.drawString(zuo+150,750,'名字:'+str(student.name))#名字
    p.drawString(zuo-5,720,'总公益时数:'+str(student.suahours)+'h')#总公益时

    location = 640
    p.drawString(zuo,680,"活动名称")
    
    p.drawString(zuo+kuan*2,680,"公益时数")
    for sua in sua_data.data:
        p.drawString(zuo,location,str(sua['activity']['title']))#活动主题
        
        p.drawString(zuo+kuan*2,location,str(sua['suahours'])+'h')#公益时数
        location -= 50
        p.line(zuo-5,location+15,you,location+15)#第N横


    p.line(zuo-5,700,you,700)#第一横
    p.line(zuo-5,655,you,655)#第二横
    p.line(zuo-5,700,zuo-5,location+15)#第一丨
    p.line(you,700,you,location+15)#第四丨
    p.line(zuo+kuan-5,700,zuo+kuan-5,location+15)#第二丨
    p.line(zuo+2*kuan-5,700,zuo+2*kuan-5,location+15)#第三丨


    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response