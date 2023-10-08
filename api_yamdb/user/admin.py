from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (
            None, {'classes': ('wide',), 'fields': (
                'username', 'email', 'password1', 'password2',
                'is_active', 'is_staff', 'role'
            )}
        ),
    )


admin.site.register(User, CustomUserAdmin)
