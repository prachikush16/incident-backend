from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, PasswordResetOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'phone', 'city', 'state', 'country', 'pincode', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'country', 'city']
    search_fields = ['email', 'username', 'phone', 'pincode']
    ordering = ['-date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'address', 'pincode', 'city', 'state', 'country')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone', 'address', 'pincode', 'city', 'state', 'country')
        }),
    )


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'created_at', 'is_used']
    list_filter = ['is_used']
    search_fields = ['user__email', 'otp']
    ordering = ['-created_at']
    readonly_fields = ['user', 'otp', 'created_at']
