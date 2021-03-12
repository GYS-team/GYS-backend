from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(StudentInfo)
admin.site.register(Activity)
admin.site.register(Sua)

