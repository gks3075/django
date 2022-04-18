from django.shortcuts import redirect, render
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
import random as rand
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    tot = article.comment_set.all().count()
    blue = article.comment_set.filter(choice='B').count()
    red = article.comment_set.filter(choice='R').count()
    if tot == 0:
        B_percent = 50
        R_percent = 50
    else:
        B_percent = blue / tot * 100
        R_percent = red / tot * 100
    context = {
        'article': article,
        'comment_form': comment_form,
        'B_percent': B_percent,
        'R_percent': R_percent,
    }
    return render(request, 'articles/detail.html', context)

def comment_create(request, pk):
    if request.user.comment_set.filter(article_id=pk).count() == 0:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.article_id = pk
                comment.save()
    return redirect('articles:detail', pk)


def random(request):
    articles = Article.objects.all()
    article = rand.choice(articles)
    return redirect('articles:detail', article.pk)