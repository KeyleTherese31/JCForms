from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser, JobseekerCV

class CustomAdminUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

admin.site.register(AdminUser, CustomAdminUserAdmin)
admin.site.register(JobseekerCV)
