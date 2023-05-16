from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from . import models
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms
from django.db.models import Q
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import DetailView
from django.contrib import messages


def articles_list(request, tag_slug=None):
    posts = Article.objects.filter(status=Article.PUBLISH).order_by('-date')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    query = request.GET.get("q")
    if query:
        posts=Article.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query), status=Article.PUBLISH).distinct()
            

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'articles/articleslist.html', {'posts':posts, 'tag':tag, 'pages':page})



# def article_detail(request, slug):
#     article = models.Article.objects.get(slug=slug)
#     return render(request, 'articles/article_detail.html',{'object':article})

class PostDetail(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'


@login_required(login_url = "/accounts/login")
def create_article(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST,request.FILES)
        if form.is_valid:
            instance = form.save(commit = False)
            instance.author = request.user
            instance.save()
            messages.success(request, instance.title +" با موفقیت ساخته شد. وضعیت: " + instance.status )
            return redirect('articles:list')
        else:
            messages.error(request, "خطا در ساخت (پر کردن تمامی فیلد ها الزامی است)")
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request , 'articles/create_article.html',{'form':form})
