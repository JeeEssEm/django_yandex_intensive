from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . import models


class ProfileInline(admin.TabularInline):
    model = models.Profile
    can_delete = False


class UserAdminModel(UserAdmin):
    inlines = (
        ProfileInline,
    )


admin.site.unregister(User)
admin.site.register(User, UserAdminModel)
