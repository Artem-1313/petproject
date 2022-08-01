from django.shortcuts import  get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Article, Comment
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,  UserPassesTestMixin
from .forms import CommentForm
from wheatherapp.utils import get_wheather
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

        return HttpResponseRedirect(reverse('newsapp:article_detail', args=[str(self.request.POST['article_id'])]))

def test(request):
    return HttpResponse("<b>Hello</b>")

class ListArticles(ListView):
    model = Article
    paginate_by = 2
    template_name = "newsapp/main.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wheather'] = get_wheather
        return context


class DetailArticle(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(article_comments=self.get_object())
        return context


class AddComment(CreateView):
    form_class = CommentForm
    template_name = "newsapp/add_comment.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        article = get_object_or_404(Article, id=self.kwargs['pk'])
        self.object.save()
        article.comments.add(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('newsapp:article_detail', kwargs={'pk': self.kwargs['pk']})



class CommentUpdate(UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']
    template_name = "newsapp/comment_update.html"

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def get_success_url(self):
        return reverse('newsapp:main')


class CommentDelete(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('newsapp:main')




