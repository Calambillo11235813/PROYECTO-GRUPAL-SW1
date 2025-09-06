from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'email', 
        'username', 
        'first_name', 
        'last_name', 
        'is_active', 
        'is_verified',
        'created_at'
    ]
    
    list_filter = [
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'is_verified',
        'created_at'
    ]
    
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'total_analyses', 
        'premium_until'
    ]
    
    list_filter = [
        'premium_until'
    ]
    
    search_fields = [
        'user__email', 
        'user__username',
        'bio'
    ]
    
    readonly_fields = ['total_analyses']
