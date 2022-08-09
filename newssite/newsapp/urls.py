from django.urls import path, include
from .views import (test, ListArticles, DetailArticle,
                    LikeArticle, AddComment, CommentUpdate,
                    CommentDelete, CategoryFilter)
from django.conf.urls.static import static
from django.conf import settings
app_name="newsapp"

urlpatterns = [

    path('', ListArticles.as_view(), name="main"),
    path('detail/<int:pk>/', DetailArticle.as_view(), name="article_detail"),
    path('article_like/<int:pk>/', LikeArticle.as_view(), name="article_like"),
    path('add_comment/<int:pk>/', AddComment.as_view(), name="comment_add"),
    path('update_comment/<int:pk>/', CommentUpdate.as_view(), name="comment_update"),
    path('delete_comment/<int:pk>/', CommentDelete.as_view(), name="comment_delete"),
    path('category/<int:pk>/', CategoryFilter.as_view(), name="category"),
    path('test/', test),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
