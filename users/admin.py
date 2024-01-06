from typing import Set
from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar', 'phone', 'is_staff', 'is_active', 'is_activated', 'date_joined')
    list_filter = ('email',)
    search_fields = ('email',)

