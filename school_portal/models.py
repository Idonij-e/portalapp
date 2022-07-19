from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max
#import secrets
import random

# Create your models here.
def generate_pk():
        num = random.randint(1000,9999)
        return 'B{}'.format(num)

class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    object=models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"Administrator"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    school_id=models.CharField(max_length=10, default=generate_pk, editable=False)

    def __str__(self):
        return self.school_id


class Administrator(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    admin_profile_pic=models.ImageField(null=True, blank = True, upload_to = "images/")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    #def save(self, **kwargs):
    #    if not self.school_id:
    #        max = Administrator.objects.aggregate(id_max=Max('school_id'))['id_max']
    #        self.school_id = "{}{:04d}".format('C', max if max is not None else 1)
    #    super().save(*kwargs)


class Staff(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    staff_profile_pic=models.ImageField(null=True, blank = True, upload_to = "images/")
    address=models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()

     #def save(self, **kwargs):
    #    if not self.school_id:
    #        max = Administrator.objects.aggregate(id_max=Max('school_id'))['id_max']
    #        self.school_id = "{}{:04d}".format('C', max if max is not None else 1)
    #    super().save(*kwargs)


#class Term(models.Model):
#    term_name=models.CharField(max_length=255)
#    objects=models.Manager()

class ClassLevel(models.Model):
    id=models.AutoField(primary_key=True)
    class_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.class_name

class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    class_id=models.ForeignKey(ClassLevel,on_delete=models.CASCADE,default=1)
    staff=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_name

class Student(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    profile_pic=models.ImageField(null=True, blank = True, upload_to = "images/")
    address=models.TextField(null=True, blank=True)
    class_id=models.ForeignKey(ClassLevel,on_delete=models.DO_NOTHING)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects = models.Manager()

    def save(self, **kwargs):
        if not self.school_id:
            max = Student.objects.aggregate(id_max=Max('school_id'))['id_max']
            self.school_id = "{}{:04d}".format('C', max if max is not None else 1)
        super().save(*kwargs)


#class StudentResult(models.Model):
#    student=models.ForeignKey(Student,on_delete=models.CASCADE)
#    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
#    subject_exam_marks=models.FloatField(default=0)
#    subject_test_marks=models.FloatField(default=0)
#    subject_assignment_marks=models.FloatField(default=0)
#    created_at=models.DateField(auto_now_add=True)
#    updated_at=models.DateField(auto_now_add=True)
#    objects=models.Manager()

#class NotificationStudent(models.Model):
#    student = models.ForeignKey(Student, on_delete=models.CASCADE)
#    message = models.TextField()
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now_add=True)
#    objects = models.Manager()


#class NotificationStaff(models.Model):
#    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#    message = models.TextField()
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now_add=True)
#    objects = models.Manager()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Administrator.objects.create(admin=instance,admin_profile_pic="")
        if instance.user_type==2:
            Staff.objects.create(admin=instance,address="",staff_profile_pic="")
        if instance.user_type==3:
            Student.objects.create(admin=instance,course_id=ClassLevel.objects.get(id=1),session_year_id=SessionYearModel.object.get(id=1),address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.administrator.save()
    if instance.user_type==2:
        instance.staff.save()
    if instance.user_type==3:
        instance.student.save()
