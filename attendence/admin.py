from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TeachersLoginInfo)
admin.site.register(Students)
admin.site.register(StudentsLoginInfo)