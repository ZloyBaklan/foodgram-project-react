
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    '''
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    '''
    list_display = ('id', 'username', 'first_name', 'last_name', 'email','password', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)
