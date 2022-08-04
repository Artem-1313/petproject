from django.contrib import admin
from .models import Article, Category, Comment
from django.contrib.admin import AdminSite
from accounts.admin import new_admin_site



# Register your models here.

@admin.register(Article, site=new_admin_site)
class ArticleAdmin(admin.ModelAdmin):


    list_display = ('title', 'likes_count', 'comments_count')
    list_filter = (
        ('categories', admin.RelatedFieldListFilter),
    )
    exclude = ('author',)
    readonly_fields = ( 'likes', )


    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()

    def likes_count(self, obj):
        return obj.sum_of_likes


    def comments_count(self, obj):
        return obj.comments_art.all().count()



    #comments_count.short_description = 'Кількість коментарів'
    likes_count.short_description = 'Кількість лайків'

    search_fields = ('title', )



@admin.register(Category, site=new_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('name',)




admin.site.site_title="Адмін-панель"

new_admin_site.register(Comment)