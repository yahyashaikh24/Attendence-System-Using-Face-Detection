from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Students(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    std = models.CharField(max_length=10)
    roll = models.IntegerField()

class TeachersLoginInfo(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    classes = models.CharField(max_length=10)
    subjects = models.CharField(max_length=10)
    time_of_login = models.DateTimeField(auto_now=True)

class StudentsLoginInfo(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeachersLoginInfo, on_delete=models.CASCADE)
    time_of_login = models.DateTimeField()