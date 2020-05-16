"""Admin"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from src.apps.user.models import User
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """custom admin for the user model"""

    ordering = ['id']
    list_display = [
        'email', 'is_verified', 'date_joined', 'is_staff', 'is_superuser'
    ]
    list_per_page = 25
    list_filter = ('is_staff', 'is_active')
    filter_horizontal = []


admin.site.unregister(Group)
