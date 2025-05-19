from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser

# Register the custom AdminUser separately to preserve the UserAdmin features
class CustomAdminUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'role')
    list_filter = ('is_superuser', 'is_staff', 'role', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

admin.site.register(AdminUser, CustomAdminUserAdmin)

# Register all other models automatically
app_models = apps.get_app_config('api').get_models()

for model in app_models:
    if model != AdminUser:  # Skip the custom user model, already registered
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
