from django.urls import path, include
from .views import test, ListArticles, DetailArticle, LikeArticle, AddComment, CommentUpdate, CommentDelete

app_name="newsapp"

urlpatterns = [

    path('', ListArticles.as_view(), name="main"),
    path('detail/<int:pk>/', DetailArticle.as_view(), name="article_detail"),
    path('article_like/<int:pk>/', LikeArticle.as_view(), name="article_like"),
    path('add_comment/<int:pk>/', AddComment.as_view(), name="comment_add"),
    path('update_comment/<int:pk>/', CommentUpdate.as_view(), name="comment_update"),
    path('delete_comment/<int:pk>/', CommentDelete.as_view(), name="comment_delete"),

]
