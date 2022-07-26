from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Article, Comment
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
# Create your views here.


class LikeArticle(LoginRequiredMixin, View):
    #redirect_field_name = 'login'

    def post(self, request, **kwargs):
        article = get_object_or_404(Article, id=self.request.POST['article_id'])
        user = self.request.user
        if user in article.likes.all():
            article.likes.remove(user)
        else:
            article.likes.add(user)

        return HttpResponseRedirect(reverse('article_detail', args=[str(self.request.POST['article_id'])]))

def test(request):
    return HttpResponse("<b>Hello</b>")


class ListArticles(ListView):
    model = Article
    paginate_by = 2
    template_name = "newsapp/main.html"


class DetailArticle(DetailView):
    model = Article



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['comment_list'] = Comment.objects.filter(article=self.get_object())
        return context


class AddComment(View):
    form_class=CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect(reverse('main'))



