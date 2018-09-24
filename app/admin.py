from django.contrib import admin
from app import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class ProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline,]
admin.site.unregister(User)
admin.site.register(User,UserProfileAdmin)

admin.site.register(models.UserProfile)
admin.site.register(models.Wlibrary)
admin.site.register(models.Relation)
admin.site.register(models.Nexus)
admin.site.register(models.Comment)
admin.site.register(models.Operator)
admin.site.register(models.Relation2)
