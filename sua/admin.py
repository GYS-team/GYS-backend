from django.contrib import admin

# Register your models here.
from .models import StudentInfo,Activity
admin.site.register(StudentInfo)
admin.site.register(Activity)
