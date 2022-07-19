from django.contrib import admin
from .models import SessionYearModel
from .models import Administrator
from .models import Staff
from .models import Student
from .models import Subject
from .models import ClassLevel


# Register your models here.
from django.contrib.auth.admin import UserAdmin

from school_portal.models import CustomUser


class UserModel(UserAdmin):
    list_display = ['school_id', 'username']

admin.site.register(CustomUser,UserModel)
admin.site.register(Administrator)
admin.site.register(SessionYearModel)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(ClassLevel)
admin.site.register(Subject)