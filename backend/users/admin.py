
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Follow

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',
                       'password1', 'password2',
                       'is_staff', 'is_active'
                       )
        }
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)