from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin)
from django.contrib.auth.models import Group as BaseGroup
from django.utils.translation import ugettext_lazy as _


from .models import User, Group

admin.site.unregister(BaseGroup)

# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': (('created_at', 'updated_at'), 'email', 'password')}),
        (_('Personal info'), {'fields': ('last_name', 'first_name', 'patronymic', 'dob', 'address', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('last_name', 'first_name', 'patronymic', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')
     
admin.site.register(User, UserAdmin)

class GroupAdmin(BaseGroupAdmin):
    pass

admin.site.register(Group, GroupAdmin)