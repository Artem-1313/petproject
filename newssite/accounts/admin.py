from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import NewUser
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.

class NewUserAdmin(UserAdmin):

    ordering = ('email',)
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = NewUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)



admin.site.register(NewUser, NewUserAdmin)
