import datetime
from django.contrib import admin
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import NewUser
from newsapp.models import Article, Comment, Subscriber
from .forms import CustomUserChangeForm, CustomUserCreationForm


class NewAdminSite(AdminSite):
    site_header = 'My Project Title'

    def index(self, request, extra_context=None):
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)

        extra_context = extra_context or {}
        extra_context['count_user'] = NewUser.objects.all().count()
        extra_context['register_user_week_ago'] = NewUser.objects.filter(date_joined__range=(week_ago, today)).count()
        extra_context['count_news'] = Article.objects.all().count()
        extra_context['all_likes'] = sum(i.likes.count() for i in Article.objects.all())
        extra_context['all_comments'] = sum(i.comments_art.all().count() for i in Article.objects.all())
        return super(NewAdminSite, self).index(request, extra_context=extra_context)


new_admin_site = NewAdminSite()


# Register your models here.
class ArticleInline(admin.StackedInline):
    model = Article
    verbose_name_plural = "Пости"
    fields = ('title', 'annotation', 'body')
    readonly_fields = ('id', 'title', 'annotation', 'body')
    can_delete = False
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    verbose_name_plural = "Коментарі користувача "
    readonly_fields = ('body', 'article',)
    can_delete = False
    extra = 0


class NewUserAdmin(UserAdmin):
    inlines = [ArticleInline, CommentInline]

    ordering = ('email',)

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'comment_count')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    search_fields = ('first_name', 'last_name')
    readonly_fields = ('first_name', 'last_name')
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('first_name', 'last_name', 'password2', 'is_staff', 'is_active',)}
         ),
    )

    def comment_count(self, obj):
        return obj.comment_set.count()

    def has_add_permission(self, request, obj=None):
        return False

    comment_count.short_description = 'Кількість коментарів'


new_admin_site.register(NewUser, NewUserAdmin)
new_admin_site.register(Subscriber)
