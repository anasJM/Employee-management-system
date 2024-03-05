from django.db import models
from django.contrib.auth.models import User

# Create your models here

class Department(models.Model):
    dep_name = models.CharField(max_length=50, null=False)
    dep_location = models.CharField(max_length=50)

    def __str__(self):
        return self.dep_name
    

class Role(models.Model):
    role_name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.role_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    first_name = models.CharField(max_length=50, null= False)
    last_name = models.CharField(max_length=50)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="employee")
    extra_bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    hire_date = models.DateField(auto_now=False, auto_now_add=False)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "%s %s" %(self.first_name, self.last_name)


class Announcement(models.Model):
    anc_title = models.CharField(max_length=100, null=False)
    anc_description = models.TextField(null=False)
    anc_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    anc_admin = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.anc_title
