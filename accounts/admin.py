from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserProfile  # or from accounts.models

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    model = UserProfile

    # Fields to display in the user list view
    list_display = ('username', 'email', 'is_instructor', 'is_student', 'is_staff')

    # Fields to filter in the sidebar
    list_filter = ('is_instructor', 'is_student', 'is_staff', 'is_superuser')

    # Sections in the user detail/edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student', 'is_instructor', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_instructor', 'phone_number'),
        }),
    )

    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
