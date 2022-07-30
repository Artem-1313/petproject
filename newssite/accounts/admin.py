from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import NewUser
from newsapp.models import Article
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Register your models here.
class ArticleInline(admin.StackedInline):
    model = Article
    fields = ('title', 'annotation', 'body')
    readonly_fields = ('title', 'annotation', 'body')


class NewUserAdmin(UserAdmin):
    inlines = [ArticleInline]
    ordering = ('email',)
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = NewUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'comment_count')
    fieldsets = (
        (None, {'fields': ( 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('first_name', 'last_name', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('first_name', 'last_name')

    def comment_count(self, obj):
        return obj.comment_set.count()
    comment_count.short_description = 'Кількість коментарів'

    def test(self, obj):
        return obj


admin.site.register(NewUser, NewUserAdmin)
