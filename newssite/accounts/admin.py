from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.template.loader import get_template

from .models import NewUser
from newsapp.models import Article, Comment
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Register your models here.
class ArticleInline(admin.StackedInline):
    model = Article
    verbose_name_plural = "Пости"
    fields = ('title', 'annotation', 'body', 'comments')
    readonly_fields = ('title', 'annotation', 'body', 'comments')
    can_delete = False
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    verbose_name_plural = "Коментарі користувача"
    readonly_fields = ('body',)
    extra = 0






class NewUserAdmin(UserAdmin):
    inlines = [ArticleInline, CommentInline]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     print(qs.filter(pk=1))
    #     return qs.filter(pk=1)

    ordering = ('email',)
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    # model = NewUser
    list_display = ('email','first_name', 'last_name', 'is_active', 'comment_count')
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

# admin.site.unregister(NewUser)
admin.site.register(NewUser, NewUserAdmin)
