from blog.models import Article, Category, Comment, Attachment
from django.template import RequestContext, loader
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.models import inlineformset_factory
from django.views.generic.dates import YearArchiveView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    latest_article_list = Article.objects.all().order_by('-pub_date')
    paginator = Paginator(latest_article_list, 20)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of rage, deliver the last page of results.
        articles = paginator.page(paginator.num_pages)

    t = loader.get_template('blog/index.html')
    c = RequestContext(request,{
        'articles': articles,
    })
    return HttpResponse(t.render(c))

def home(request):
    nav_bar = Category.objects.filter(flat=True).exclude(name="Welcome").order_by('pub_date')
    home_announce = Article.objects.filter(category__name='Announcement').order_by('-pub_date')[:5]
    home_welcome = Article.objects.filter(category__name="Welcome")[:5]
    t = loader.get_template('home.html')
    c = RequestContext(request,{
        'nav_bar':nav_bar,
        'home_welcome':home_welcome,
        'home_announce':home_announce,
    })
    return HttpResponse(t.render(c))

def home_article(request, category_id):
    category = Category.objects.get(pk=category_id)
    nav_bar = Category.objects.filter(flat=True).exclude(name="Welcome").order_by('pub_date')
    try:
        home_article = Article.objects.filter(category=category_id).order_by('-pub_date')[:5] 
    except Article.DoesNotExist:
        raise Http404
    t = loader.get_template('home_article.html')
    c = RequestContext(request,{
        'home_article':home_article,
        'nav_bar':nav_bar,
        'category':category,
    })
    return HttpResponse(t.render(c))

def category(request):
    category_list = Category.objects.all().order_by('pub_date')
    t = loader.get_template('blog/category.html')
    c = RequestContext(request,{
        'category_list': category_list
    })
    return HttpResponse(t.render(c))

def category_article(request, category_id):
    category = Category.objects.get(pk=category_id)
    try:
        article_by_category = Article.objects.filter(category=category_id).order_by('-pub_date')[:20]
    except Article.DoesNotExist:
        raise Http404
    t = loader.get_template('blog/category_article.html')
    c = RequestContext(request, {
        'article_by_category': article_by_category,
        'category':category,
    })
    return HttpResponse(t.render(c))

def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404

    comment_in_article = Comment.objects.filter(article=article_id).order_by('-pub_date')[:20]
    CommentFormSet = inlineformset_factory(Article, Comment, extra=1, can_delete=False)
    if request.method == 'POST':
        formset = CommentFormSet(request.POST, request.FILES, instance=article)
        if formset.is_valid():
            formset.save()
            formset.cleaned_data
            return HttpResponseRedirect('')
            
    else:
        formset = CommentFormSet()

    t = loader.get_template('blog/detail.html')
    c = RequestContext(request,{
        'article':article,
        "formset": formset,
        'comment_in_article': comment_in_article,
    })
    return HttpResponse(t.render(c))

def attachment(request, article_id):
    try:
        article = Article.objects.get(pk=article_id) 
    except Article.DoesNotExist:
        raise Http404
    attachment_in_article = Attachment.objects.filter(article=article_id)

    t = loader.get_template('blog/attachment.html')
    c = RequestContext(request,{
        'article':article,
        'attachment_in_article':attachment_in_article,
    })
    return HttpResponse(t.render(c))

def archive_index(request):
    '''a basic articles listing view'''
    articles = Article.objects.filter().order_by('-pub_date')
    now = datetime.datetime.now()
 
    #create a dict with the years and months:articles 
    article_dict = {}
    for i in range(articles[0].pub_date.year, articles[len(articles)-1].pub_date.year-1, -1):
        article_dict[i] = {}
        for month in range(12,0,-1):
            article_dict[i][month] = []
    for article in articles:
        article_dict[article.pub_date.year][article.pub_date.month].append(article)
 
    #this is necessary for the years to be sorted
    article_sorted_keys = list(reversed(sorted(article_dict.keys())))
    list_articles = []
    for key in article_sorted_keys:
        adict = {key:article_dict[key]}
        list_articles.append(adict)
 
    t = loader.get_template('blog/archive_index.html')
    c = RequestContext(request,{
       'now': now,'list_articles':list_articles,
    })
    return HttpResponse(t.render(c))

def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            articles = Article.objects.filter(title__icontains=q).order_by("-pub_date")
            t = loader.get_template('blog/search_results.html')
            c = RequestContext(request,{
                'articles':articles, 'query':q
            })
            return HttpResponse(t.render(c))
    t = loader.get_template('blog/search_form.html')
    c = RequestContext(request,{
        'error':error
    })
    return HttpResponse(t.render(c))

class ArticleYearArchiveView(YearArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True
